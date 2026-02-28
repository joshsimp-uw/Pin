from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from app.api.deps import bearer_token
from app.core.auth import require_user
from app.core.config import settings
from app.core.repository import ensure_org, ensure_user, insert_message, insert_ticket, link_session_to_ticket, close_session, set_session_title
from app.core.session import SessionState, load_session, new_session, save_session
from app.flows.engine import question_for, registry, next_missing_field
from app.knowledge.support import is_supported_request
from app.llm.providers import LLMError, get_llm
from app.models.schemas import AnswerResponse, ActionResponse, Action, ChatRequest, ChatResponse, Ticket, TicketResponse
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


async def _llm_field_extract(message: str, required_fields: list[str], org_id: str) -> dict[str, Any]:
    """Use the LLM to intelligently extract missing required fields from the user's message."""
    if not required_fields:
        return {}
    
    # Gemini requires uppercase types for its schema
    schema = {
        "type": "OBJECT",
        "properties": {
            field: {"type": "STRING"} for field in required_fields
        }
    }
    
    prompt = (
        f"Extract the following fields from the user's IT support request if they are present: {', '.join(required_fields)}.\n"
        f"User message: '{message}'\n"
        "Only extract values explicitly mentioned or clearly implied. For example, if they mention an iPhone, the OS is iOS. "
        "Leave fields out or set to null if you are unsure."
    )
    
    llm = get_llm(org_id=org_id)
    try:
        result_str = await llm.chat([{"role": "user", "content": prompt}], response_format=schema)
        return json.loads(result_str)
    except Exception as e:
        print(f"LLM Extraction failed: {e}")
        return {} # Fallback to empty if LLM fails


# Change definition to async and pass org_id
async def _merge_collected(state: SessionState, req: ChatRequest, org_id: str) -> None:
    # 1) Parse explicit kv fields first
    kv = _extract_kv(req.message)
    for k, v in kv.items():
        if k not in state.collected:
            state.collected[k] = v

    # 2) LLM guesses for missing required fields
    flow = registry.get(state.category)
    required = list(getattr(flow, "required_fields", []) or [])
    missing = [f for f in required if f not in state.collected]
    
    if missing:
        guessed = await _llm_field_extract(req.message, required_fields=missing, org_id=org_id)
        for k, v in guessed.items():
            if k not in state.collected and v is not None and str(v).strip() != "":
                state.collected[k] = v

    # 3) Accept explicit context from client as collected
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
    """Chat with the assistant."""
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

    state = load_session(req.session_id) if req.session_id else new_session(org_id=u.org_id, user_id=u.user_id)
    if state.org_id != u.org_id or state.user_id != u.user_id:
        raise HTTPException(status_code=403, detail="Session does not belong to the current user")
    if state.status != "open":
        raise HTTPException(status_code=400, detail="Chat is closed. Start a new chat to continue.")
    state.turns += 1

    if not state.category:
        state.category = registry.classify(req.message)

    flow = registry.get(state.category)

    # 1. NEW: Call the async merge function using the LLM
    await _merge_collected(state, req, u.org_id)

    insert_message(session_id=state.session_id, role="user", content=req.message)

    if not state.title:
        first = req.message.strip().split("\n", 1)[0].strip()
        if first:
            state.title = first[:80]
            try:
                set_session_title(state.session_id, state.title)
            except Exception:
                pass

    pending = (state.collected or {}).get("_pending_action")
    if pending:
        msg = req.message.strip().lower()
        yes = msg in {"y","yes","yeah","yep","ok","okay","sure","do it","please"} or msg.startswith("yes")
        no = msg in {"n","no","nope","not now","cancel"} or msg.startswith("no")
        if yes:
            if pending.get("type") == "close_chat":
                close_session(state.session_id)
                state.status = "closed"
                state.collected.pop("_pending_action", None)
                save_session(state)
                return AnswerResponse(message="Closed this chat. If you need anything else, start a new issue.", citations=[], collected=state.collected)
            if pending.get("type") == "escalate_to_ticket":
                draft = pending.get("draft") or {}
                ticket = Ticket(**draft)
                rendered = _render_ticket(ticket)
                ticket_id = insert_ticket(
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
                link_session_to_ticket(state.session_id, ticket_id)
                state.ticket_id = ticket_id
                state.collected.pop("_pending_action", None)
                save_session(state)
        if no:
            state.collected.pop("_pending_action", None)
            save_session(state)
        else:
            prompt = str(pending.get("prompt") or "Please reply yes or no.")
            insert_message(session_id=state.session_id, role="assistant", content=prompt)
            save_session(state)
            return ActionResponse(message=prompt, actions=[Action(action_id="yes", label="Yes"), Action(action_id="no", label="No")], meta={"pending": pending.get("type")})

    msg_l = req.message.strip().lower()
    if any(k in msg_l for k in ["resolved", "fixed", "that worked", "solved", "thank you", "thanks", "thx"]):
        prompt = "Glad to hear it. Would you like to close this chat?"
        state.collected["_pending_action"] = {"type": "close_chat", "prompt": prompt}
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        return ActionResponse(message=prompt, actions=[Action(action_id="yes", label="Close chat"), Action(action_id="no", label="Keep open")], meta={"pending": "close_chat"})

    missing = next_missing_field(flow, state.collected)
    if missing:
        q = question_for(flow, missing)
        insert_message(session_id=state.session_id, role="assistant", content=q)
        save_session(state)
        return AnswerResponse(
            message=q,
            citations=[],
            next_question=q,
            collected=state.collected,
        )

    # 2. IMPROVE RETRIEVAL: LLM Query Rewriting
    llm = get_llm(org_id=u.org_id)
    rewrite_prompt = (
        "Rewrite the following IT support issue and gathered context into a concise, keyword-rich semantic search query. "
        "Do not include conversational filler, just the core technical entities, errors, and intent.\n"
        f"User Issue: {req.message}\n"
        f"Context: {state.collected}"
    )
    
    try:
        query = await llm.chat([{"role": "user", "content": rewrite_prompt}])
    except Exception:
        # Fallback if the LLM fails
        query = req.message + "\n" + "\n".join([f"{k}: {v}" for k, v in sorted(state.collected.items())])

    citations, best_score = await retrieve(query, org_id=u.org_id)

    # 3. Softened escalation: Escalate based on retrieval score and turns, not hardcoded paths
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
        prompt = (
            "I’m not confident we can resolve this safely with the KB excerpts I have. "
            "Would you like to escalate this chat to a ticket?"
        )
        state.collected["_pending_action"] = {
            "type": "escalate_to_ticket",
            "prompt": prompt,
            "draft": ticket.model_dump(),
        }
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        return ActionResponse(
            message=prompt,
            actions=[Action(action_id="escalate", label="Escalate to ticket"), Action(action_id="no", label="Keep chatting")],
            meta={"pending": "escalate_to_ticket"},
        )

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
        prompt = (
            "I can’t answer that safely under our guardrails. "
            "Would you like to escalate this chat to a ticket for a technician to review?"
        )
        state.collected["_pending_action"] = {
            "type": "escalate_to_ticket",
            "prompt": prompt,
            "draft": ticket.model_dump(),
        }
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        return ActionResponse(
            message=prompt,
            actions=[Action(action_id="escalate", label="Escalate to ticket"), Action(action_id="no", label="Keep chatting")],
            meta={"pending": "escalate_to_ticket"},
        )

    insert_message(
        session_id=state.session_id,
        role="assistant",
        content=content,
        citations=[c.model_dump() for c in citations],
    )
    save_session(state)
    return AnswerResponse(message=content, citations=citations, collected=state.collected)
