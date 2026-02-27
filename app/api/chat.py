from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from app.api.deps import bearer_token
from app.core.auth import require_user
from app.core.config import settings
from app.core.repository import ensure_org, ensure_user, insert_message, insert_ticket
from app.core.session import SessionState, load_session, new_session, save_session
from app.flows.engine import question_for, registry, next_missing_field
from app.knowledge.support import is_supported_request
from app.llm.providers import LLMError, get_llm
from app.models.schemas import AnswerResponse, ChatRequest, ChatResponse, Ticket, TicketResponse
from app.policies.guardrails import check_response, should_escalate
from app.rag.index import retrieve

router = APIRouter(tags=["chat"])


# ---------------------------
# Helpers (moved from app/main.py)
# ---------------------------

def _extract_kv(message: str) -> dict[str, str]:
    """Parse user-provided key/value fields.

    Supported formats:
      os: Windows 11
      error_message = 809
    """
    out: dict[str, str] = {}
    for line in message.splitlines():
        m = re.match(r"^\s*([a-zA-Z_][a-zA-Z0-9_]{1,40})\s*[:=]\s*(.+?)\s*$", line)
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


def _heuristic_field_guess(message: str, required_fields: list[str] | None = None) -> dict[str, Any]:
    """Heuristically infer answers to flow questions from natural language.

    Returns only fields we can confidently extract.
    If required_fields is provided, we limit inference to those names to avoid extra noise.
    """

    text = message.strip()
    t = text.lower()
    wants: set[str] | None = set(required_fields) if required_fields else None
    out: dict[str, Any] = {}

    def need(name: str) -> bool:
        return True if wants is None else (name in wants)

    # ---------------------------
    # Common helpers
    # ---------------------------
    YES = {"yes", "y", "yeah", "yep", "works", "working", "ok", "okay", "fine", "success"}
    NO = {
        "no",
        "n",
        "nope",
        "not",
        "doesnt",
        "doesn't",
        "cant",
        "can't",
        "cannot",
        "broken",
        "fails",
        "failing",
        "failed",
        "error",
    }
    UNSURE = {"unsure", "maybe", "not sure", "unknown", "don't know", "dont know", "idk"}

    def norm_yes_no(txt: str) -> str | None:
        w = txt.lower()
        if any(wd in w for wd in YES):
            return "yes"
        if any(wd in w for wd in NO):
            return "no"
        if any(wd in w for wd in UNSURE):
            return "unsure"
        return None

    # ---------------------------
    # summary  (fallback flow)
    # ---------------------------
    if need("summary"):
        # First sentence up to 120 chars, for concise summaries
        import re as _re

        first = _re.split(r"[.\n]", text, maxsplit=1)[0].strip()
        if first:
            out.setdefault("summary", first[:120])

    # ---------------------------
    # os  (used in multiple flows)
    # ---------------------------
    if need("os"):
        if re.search(r"\bwin(dows)?\s*11\b", t):
            out.setdefault("os", "Windows 11")
        elif re.search(r"\bwin(dows)?\s*10\b", t):
            out.setdefault("os", "Windows 10")
        elif "windows" in t:
            out.setdefault("os", "Windows")
        elif any(k in t for k in ["macos", "os x", "osx", "mac"]):
            out.setdefault("os", "macOS")
        elif any(k in t for k in ["ubuntu", "debian", "mint", "linux"]):
            out.setdefault("os", "Linux")
        elif any(k in t for k in ["iphone", "ipad", "ios"]):
            out.setdefault("os", "iOS")
        elif "android" in t:
            out.setdefault("os", "Android")

    # ---------------------------
    # device_type  (fallback, vpn, wifi)
    # ---------------------------
    if need("device_type"):
        if any(k in t for k in ["laptop", "notebook", "macbook", "thinkpad"]):
            out.setdefault("device_type", "laptop")
        elif any(k in t for k in ["desktop", "workstation", "tower"]):
            out.setdefault("device_type", "desktop")
        elif any(k in t for k in ["phone", "mobile", "cell", "iphone", "android"]):
            out.setdefault("device_type", "phone")
        elif any(k in t for k in ["ipad", "tablet"]):
            out.setdefault("device_type", "tablet")

    # ---------------------------
    # network_type  (vpn)
    # ---------------------------
    if need("network_type"):
        if any(k in t for k in ["hotspot", "tether", "cellular", "lte", "5g"]):
            out.setdefault("network_type", "mobile hotspot")
        elif any(k in t for k in ["office", "on-site", "onsite", "campus", "corporate"]):
            out.setdefault("network_type", "on-site network")
        elif any(k in t for k in ["home", "house", "apartment"]):
            out.setdefault("network_type", "home wi-fi")
        elif any(k in t for k in ["wifi", "wi-fi", "wireless", "ssid"]):
            out.setdefault("network_type", "wi-fi")

    # ---------------------------
    # error_message  (vpn, wifi)
    # ---------------------------
    if need("error_message"):
        # Quoted phrases or "error ..." fragments or numeric codes
        m = re.search(r"\berror(?:\s*code)?\s*[:#]?\s*([A-Za-z0-9._-]{2,})", text, flags=re.I)
        if m:
            out.setdefault("error_message", m.group(0).strip())
        else:
            # Common phrasing like "No Internet", "Connected without Internet"
            m2 = re.search(
                r"\b(no internet|connected without internet|authentication failed|timed out)\b",
                t,
                flags=re.I,
            )
            if m2:
                out.setdefault("error_message", m2.group(0))
            else:
                m3 = re.search(r"\b\d{3,5}\b", text)  # numeric error code alone
                if m3:
                    out.setdefault("error_message", f"error {m3.group(0)}")

    # ---------------------------
    # mfa_working  (vpn)
    # ---------------------------
    if need("mfa_working"):
        if any(k in t for k in ["mfa", "2fa", "two-factor", "authenticator"]):
            v = norm_yes_no(t)
            if v:
                out.setdefault("mfa_working", v)
        # "I can sign into other apps" → infer yes
        if "other" in t and any(k in t for k in ["works", "working", "ok", "okay", "fine"]):
            out.setdefault("mfa_working", "yes")

    # ---------------------------
    # client  (email)
    # ---------------------------
    if need("client"):
        if any(k in t for k in ["outlook desktop", "outlook app"]):
            out.setdefault("client", "Outlook")
        elif any(k in t for k in ["outlook", "owa", "webmail", "browser"]):
            out.setdefault("client", "OWA")
        elif any(k in t for k in ["apple mail", "mail.app", "mail app"]):
            out.setdefault("client", "Apple Mail")
        elif any(k in t for k in ["gmail app", "android mail", "iphone mail", "ios mail", "mobile app"]):
            out.setdefault("client", "mobile app")

    # ---------------------------
    # symptom  (email)
    # ---------------------------
    if need("symptom"):
        if any(
            k in t
            for k in ["can't sign in", "cant sign in", "signin", "sign in", "login", "log in", "auth"]
        ):
            out.setdefault("symptom", "can't sign in")
        elif any(k in t for k in ["missing mail", "email missing", "disappeared", "can't find", "cant find"]):
            out.setdefault("symptom", "missing mail")
        elif any(k in t for k in ["bounce", "bounced", "undeliverable", "nondelivery", "ndr"]):
            out.setdefault("symptom", "bounce")
        elif any(k in t for k in ["delay", "delayed", "slow delivery", "late"]):
            out.setdefault("symptom", "delayed delivery")

    # ---------------------------
    # scope  (email)
    # ---------------------------
    if need("scope"):
        if any(k in t for k in ["only me", "just me", "my account", "i'm the only one", "im the only one"]):
            out.setdefault("scope", "just me")
        elif any(k in t for k in ["everyone", "all users", "team", "multiple", "others too", "widespread"]):
            out.setdefault("scope", "multiple users")
        elif any(k in t for k in ["unsure", "not sure", "idk", "unknown"]):
            out.setdefault("scope", "unsure")

    # ---------------------------
    # location  (wifi)
    # ---------------------------
    if need("location"):
        if any(k in t for k in ["office", "on-site", "onsite", "campus", "work"]):
            out.setdefault("location", "on-site")
        elif any(k in t for k in ["home", "house", "apartment"]):
            out.setdefault("location", "home")
        elif any(k in t for k in ["coffee", "hotel", "airport", "public"]):
            out.setdefault("location", "public")

    # ---------------------------
    # scope  (wifi)
    # ---------------------------
    if need("scope"):
        if any(k in t for k in ["only me", "just me", "my laptop", "my phone"]):
            out.setdefault("scope", "single device")
        elif any(k in t for k in ["everyone", "all", "whole", "entire", "building", "floor"]):
            out.setdefault("scope", "multiple users")

    # ---------------------------
    # in_office  (printer)
    # ---------------------------
    if need("in_office"):
        if any(k in t for k in ["in office", "at work", "on site", "onsite", "campus"]):
            out.setdefault("in_office", "yes")
        elif any(k in t for k in ["remote", "at home", "home"]):
            out.setdefault("in_office", "no")

    # ---------------------------
    # printer_name  (printer)
    # ---------------------------
    if need("printer_name"):
        m = re.search(r"\bprinter\s+([A-Za-z0-9._-]{2,})\b", text, flags=re.I)
        if m:
            out.setdefault("printer_name", m.group(1))

    # ---------------------------
    # print_queue  (printer)
    # ---------------------------
    if need("print_queue"):
        m = re.search(r"\b(queue|print queue)\s*[:#]?\s*([A-Za-z0-9._-]{2,})\b", text, flags=re.I)
        if m:
            out.setdefault("print_queue", m.group(2))

    # ---------------------------
    # issue_type (printer)
    # ---------------------------
    if need("issue_type"):
        if any(k in t for k in ["stuck", "queued", "pending", "won't print", "cant print", "can't print"]):
            out.setdefault("issue_type", "stuck queue")
        elif any(k in t for k in ["offline", "not responding"]):
            out.setdefault("issue_type", "offline")
        elif any(k in t for k in ["driver", "install"]):
            out.setdefault("issue_type", "driver")

    return out


def _merge_collected(state: SessionState, req: ChatRequest) -> None:
    # 1) Parse explicit kv fields first
    kv = _extract_kv(req.message)
    for k, v in kv.items():
        if k not in state.collected:
            state.collected[k] = v

    # 2) Heuristic guesses, but only for missing required fields
    flow = registry.get(state.category)
    required = list(getattr(flow, "required_fields", []) or [])
    missing = [f for f in required if f not in state.collected]
    if missing:
        guessed = _heuristic_field_guess(req.message, required_fields=missing)
        for k, v in guessed.items():
            if k not in state.collected and v is not None:
                state.collected[k] = v

    # 3) Accept explicit context from client as collected (safe fields)
    # Allow "context" fields to be promoted into collected if they match required.
    if req.context:
        for k, v in req.context.items():
            kk = str(k).strip().lower()
            if kk in missing and v is not None:
                state.collected.setdefault(kk, v)


def _render_ticket(t: Ticket) -> str:
    lines: list[str] = []
    lines.append("TICKET CREATED")
    lines.append("=")
    lines.append(f"Summary: {t.summary}")
    lines.append(f"Category: {t.category}")
    if t.impact:
        lines.append(f"Impact: {t.impact}")
    if t.urgency:
        lines.append(f"Urgency: {t.urgency}")
    lines.append("")
    lines.append("User:")
    for k, v in (t.user or {}).items():
        lines.append(f"  {k}: {v}")
    if t.device:
        lines.append("")
        lines.append("Device:")
        for k, v in (t.device or {}).items():
            lines.append(f"  {k}: {v}")
    if t.diagnostics:
        lines.append("")
        lines.append("Diagnostics:")
        for k, v in (t.diagnostics or {}).items():
            lines.append(f"  {k}: {v}")
    if t.steps_attempted:
        lines.append("")
        lines.append("Steps attempted:")
        for s in t.steps_attempted:
            lines.append(f"  - {s}")
    lines.append("")
    lines.append(f"Escalation reason: {t.escalation_reason}")
    if t.citations:
        lines.append("")
        lines.append("Sources:")
        for c in t.citations:
            lines.append(f"  - {c.source_id} :: {c.title}")
    return "\n".join(lines).strip() + "\n"


# ---------------------------
# Routes
# ---------------------------


@router.post("/session/new")
def create_session(authorization: str | None = Header(default=None)) -> dict[str, str]:
    """Create a new chat session for the authenticated user."""
    u = require_user(bearer_token(authorization))
    ensure_org(u.org_id, name=u.org_id)
    ensure_user(
        org_id=u.org_id,
        user_id=u.user_id,
        first_name=u.first_name,
        last_name=u.last_name,
        email=u.email,
        role=u.role,
    )
    s = new_session(org_id=u.org_id, user_id=u.user_id)
    return {"session_id": s.session_id}


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, authorization: str | None = Header(default=None)):
    """Chat with the assistant.

    Org/user are derived from the authenticated session (Bearer token). This prevents
    callers from spoofing org_id/user_id and ensures RAG + LLM settings resolve
    against the correct org configuration from the admin portal.
    """
    u = require_user(bearer_token(authorization))

    # Ensure org/user exist (idempotent). In a per-org DB deployment, org_id is typically constant.
    ensure_org(u.org_id, name=u.org_id)
    ensure_user(
        org_id=u.org_id,
        user_id=u.user_id,
        first_name=u.first_name,
        last_name=u.last_name,
        email=u.email,
        role=u.role,
    )

    # Load or create session (must belong to the authenticated user)
    state = load_session(req.session_id) if req.session_id else new_session(org_id=u.org_id, user_id=u.user_id)
    if state.org_id != u.org_id or state.user_id != u.user_id:
        raise HTTPException(status_code=403, detail="Session does not belong to the current user")
    state.turns += 1

    # Categorize once (sticky)
    if not state.category:
        state.category = registry.classify(req.message)

    flow = registry.get(state.category)

    # Merge user/context info into collected fields
    _merge_collected(state, req)

    # Persist user message (chat transcript)
    insert_message(session_id=state.session_id, role="user", content=req.message)

    # Gate: required fields
    missing = next_missing_field(flow, state.collected)
    if missing:
        q = question_for(flow, missing)
        # Persist assistant prompt/question
        insert_message(session_id=state.session_id, role="assistant", content=q)
        save_session(state)
        return AnswerResponse(
            message=q,
            citations=[],
            next_question=q,
            collected=state.collected,
        )

    # If the user is asking about an unsupported device/OS/app, escalate immediately.
    supported, unsupported_reason = is_supported_request(
        message=req.message,
        category=state.category or "unknown",
        collected=state.collected,
        kb_dir=Path(settings.kb_dir),
    )
    if not supported:
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={
                "org_id": u.org_id,
                "user_id": u.user_id,
                **{k: v for k, v in req.context.items() if k.startswith("user_")},
            },
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason=unsupported_reason or "Unsupported device/OS/application",
            citations=[],
        )
        rendered = _render_ticket(ticket)
        insert_ticket(
            org_id=u.org_id,
            user_id=u.user_id,
            session_id=state.session_id,
            summary=ticket.summary,
            category=ticket.category,
            impact=ticket.impact,
            urgency=ticket.urgency,
            escalation_reason=ticket.escalation_reason,
            rendered_text=rendered,
            diagnostics=ticket.diagnostics,
            steps_attempted=ticket.steps_attempted,
            citations=[],
        )
        insert_message(session_id=state.session_id, role="assistant", content=rendered)
        save_session(state)
        return TicketResponse(ticket=ticket, rendered=rendered)

    # Retrieve docs based on message + collected context
    query = req.message + "\n" + "\n".join([f"{k}: {v}" for k, v in sorted(state.collected.items())])
    citations, best_score = await retrieve(query, org_id=u.org_id)

    # Decide escalation
    esc, esc_reason = should_escalate(state.turns, best_score)
    if esc:
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={
                "org_id": u.org_id,
                "user_id": u.user_id,
                **{k: v for k, v in req.context.items() if k.startswith("user_")},
            },
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason=esc_reason or "Escalated",
            citations=citations,
        )
        rendered = _render_ticket(ticket)
        insert_ticket(
            org_id=u.org_id,
            user_id=u.user_id,
            session_id=state.session_id,
            summary=ticket.summary,
            category=ticket.category,
            impact=ticket.impact,
            urgency=ticket.urgency,
            escalation_reason=ticket.escalation_reason,
            rendered_text=rendered,
            diagnostics=ticket.diagnostics,
            steps_attempted=ticket.steps_attempted,
            citations=[c.model_dump() for c in ticket.citations],
        )
        insert_message(session_id=state.session_id, role="assistant", content=rendered)
        save_session(state)
        return TicketResponse(ticket=ticket, rendered=rendered)

    # Compose prompt grounded in citations
    system = (
        "You are a Tier 0/Tier 1 IT support technician for a single company. "
        "Stay in scope. Use ONLY the provided KB excerpts as your source of truth. "
        "If the KB does not contain a safe/clear procedure, say you will escalate. "
        "Ask concise follow-up questions only if absolutely required. "
        "Never ask for passwords or secrets."
    )

    kb_block = "\n\n".join([f"SOURCE {i+1}: {c.title}\n{c.snippet}" for i, c in enumerate(citations)])
    user = (
        f"User issue:\n{req.message}\n\n"
        f"Collected context:\n" + "\n".join([f"- {k}: {v}" for k, v in sorted(state.collected.items())]) + "\n\n"
        f"KB excerpts (use these, cite by SOURCE #):\n{kb_block}\n\n"
        "Respond with: (1) a short diagnosis, (2) numbered steps, (3) what to report back."
    )

    llm = get_llm(org_id=u.org_id)
    try:
        content = await llm.chat(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))

    gr = check_response(content)
    if not gr.ok:
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={"org_id": u.org_id, "user_id": u.user_id},
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason=f"Guardrail blocked response: {gr.reason}",
            citations=citations,
        )
        rendered = _render_ticket(ticket)
        insert_ticket(
            org_id=u.org_id,
            user_id=u.user_id,
            session_id=state.session_id,
            summary=ticket.summary,
            category=ticket.category,
            impact=ticket.impact,
            urgency=ticket.urgency,
            escalation_reason=ticket.escalation_reason,
            rendered_text=rendered,
            diagnostics=ticket.diagnostics,
            steps_attempted=ticket.steps_attempted,
            citations=[c.model_dump() for c in ticket.citations],
        )
        insert_message(session_id=state.session_id, role="assistant", content=rendered)
        save_session(state)
        return TicketResponse(ticket=ticket, rendered=rendered)

    insert_message(
        session_id=state.session_id,
        role="assistant",
        content=content,
        citations=[c.model_dump() for c in citations],
    )
    save_session(state)
    return AnswerResponse(message=content, citations=citations, collected=state.collected)
