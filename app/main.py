from __future__ import annotations

import re
from typing import Any

from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.core.db import init_schema
from app.core.repository import ensure_org, ensure_user, insert_message, insert_ticket
from app.core.session import SessionState, load_session, new_session, save_session
from app.flows.engine import question_for, registry, next_missing_field
from app.llm.providers import LLMError, get_llm
from app.models.schemas import AnswerResponse, ChatRequest, ChatResponse, Ticket, TicketResponse
from app.policies.guardrails import check_response, should_escalate
from app.rag.index import load_index, retrieve

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def _startup() -> None:
    # Create/upgrade schema for this org site's SQLite database.
    init_schema()


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


def _heuristic_field_guess(message: str) -> dict[str, Any]:
    m = message.lower()
    guessed: dict[str, Any] = {}
    if "windows" in m:
        guessed["os"] = "Windows"
    elif "macos" in m or "mac os" in m or "osx" in m or "os x" in m or "mac" in m:
        guessed["os"] = "macOS"
    elif "android" in m:
        guessed["os"] = "Android"
    elif "iphone" in m or "ipad" in m or "ios" in m:
        guessed["os"] = "iOS"
    elif "linux" in m or "ubuntu" in m or "debian" in m or "mint" in m:
        guessed["os"] = "Linux"

    # Common yes/no
    if re.search(r"\b(mfa|2fa)\b.*\b(yes|works|working)\b", m):
        guessed["mfa_working"] = "yes"
    if re.search(r"\b(mfa|2fa)\b.*\b(no|broken|fails|failing)\b", m):
        guessed["mfa_working"] = "no"

    return guessed


def _merge_collected(state: SessionState, req: ChatRequest) -> None:
    # 1) take explicit context (from auth/LDAP/etc.)
    for k, v in (req.context or {}).items():
        if v is None:
            continue
        state.collected.setdefault(k, v)

    # 2) parse key/value lines from the user message
    kv = _extract_kv(req.message)
    for k, v in kv.items():
        state.collected[k] = v

    # 3) heuristic guesses
    guessed = _heuristic_field_guess(req.message)
    for k, v in guessed.items():
        state.collected.setdefault(k, v)


def _render_ticket(t: Ticket) -> str:
    lines = []
    lines.append(f"Summary: {t.summary}")
    lines.append(f"Category: {t.category}")
    lines.append(f"Impact/Urgency: {t.impact}/{t.urgency}")
    lines.append("")
    lines.append("User:")
    for k, v in t.user.items():
        lines.append(f"  - {k}: {v}")
    lines.append("Device:")
    for k, v in t.device.items():
        lines.append(f"  - {k}: {v}")
    lines.append("")
    lines.append("Diagnostics:")
    for k, v in t.diagnostics.items():
        lines.append(f"  - {k}: {v}")
    if t.error_text:
        lines.append("")
        lines.append("Error:")
        lines.append(t.error_text)
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/session/new")
def create_session() -> dict[str, str]:
    s = new_session(org_id='demo-org', user_id='demo-user')
    return {"session_id": s.session_id}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Ensure org/user exist (idempotent). In a per-org DB deployment, org_id is typically constant.
    ensure_org(req.org_id, name=req.org_id)
    ensure_user(org_id=req.org_id, user_id=req.user_id)

    # Load or create session
    state = load_session(req.session_id) if req.session_id else new_session(org_id=req.org_id, user_id=req.user_id)
    state.turns += 1

    # Categorize once (sticky)
    if not state.category:
        state.category = registry.classify(req.message)

    flow = registry.get(state.category)

    # Merge user/context info into collected fields
    _merge_collected(state, req)

    # Persist user message (chat transcript)
    insert_message(session_id=state.session_id, role='user', content=req.message)

    # Gate: required fields
    missing = next_missing_field(flow, state.collected)
    if missing:
        q = question_for(flow, missing)
        # Persist assistant prompt/question
        insert_message(session_id=state.session_id, role='assistant', content=q)
        save_session(state)
        return AnswerResponse(
            message=q,
            citations=[],
            next_question=q,
            collected=state.collected,
        )

    # Load RAG index
    try:
        index = load_index()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Retrieve docs based on message + collected context
    query = req.message + "\n" + "\n".join([f"{k}: {v}" for k, v in sorted(state.collected.items())])
    citations, best_score = retrieve(index, query)

    # Decide escalation
    esc, esc_reason = should_escalate(state.turns, best_score)
    if esc:
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={"org_id": req.org_id, "user_id": req.user_id, **{k: v for k, v in req.context.items() if k.startswith("user_")}},
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason=esc_reason or "Escalated",
            citations=citations,
        )
        rendered = _render_ticket(ticket)
        insert_ticket(
            org_id=req.org_id,
            user_id=req.user_id,
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
        insert_message(session_id=state.session_id, role='assistant', content=rendered)
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

    llm = get_llm()
    try:
        content = await llm.chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))

    gr = check_response(content)
    if not gr.ok:
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={"org_id": req.org_id, "user_id": req.user_id},
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason=f"Guardrail blocked response: {gr.reason}",
            citations=citations,
        )
        rendered = _render_ticket(ticket)
        insert_ticket(
            org_id=req.org_id,
            user_id=req.user_id,
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
        insert_message(session_id=state.session_id, role='assistant', content=rendered)
        save_session(state)
        return TicketResponse(ticket=ticket, rendered=rendered)

    insert_message(session_id=state.session_id, role='assistant', content=content, citations=[c.model_dump() for c in citations])
    save_session(state)
    return AnswerResponse(message=content, citations=citations, collected=state.collected)