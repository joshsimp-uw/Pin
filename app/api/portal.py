from __future__ import annotations

from fastapi import APIRouter, Body, Header, HTTPException

from app.api.deps import bearer_token
from app.core.auth import require_user
from app.core.repository import (
    close_session,
    get_session,
    get_ticket,
    link_session_to_ticket,
    list_session_messages,
    list_ticket_sessions,
    list_user_sessions,
    list_user_tickets,
)
from app.core.session import load_session, save_session
from app.api.chat import _render_ticket  # reuse renderer
from app.models.schemas import Ticket
from app.core.repository import insert_ticket

router = APIRouter(tags=["portal"])


@router.get("/api/home")
def home_summary(authorization: str | None = Header(default=None)) -> dict:
    u = require_user(bearer_token(authorization))

    open_chats = list_user_sessions(u.org_id, u.user_id, "open", limit=50)
    closed_chats = list_user_sessions(u.org_id, u.user_id, "closed", limit=50)
    open_tickets = list_user_tickets(u.org_id, u.user_id, "created", limit=50)
    closed_tickets = list_user_tickets(u.org_id, u.user_id, "closed", limit=50)

    return {
        "counts": {
            "open_chats": len(open_chats),
            "closed_chats": len(closed_chats),
            "open_tickets": len(open_tickets),
            "closed_tickets": len(closed_tickets),
        },
        "recent": {
            "open_chats": open_chats[:10],
            "open_tickets": open_tickets[:10],
        },
    }


@router.get("/api/chats")
def chats_list(status: str = "open", authorization: str | None = Header(default=None)) -> list[dict]:
    u = require_user(bearer_token(authorization))
    status = (status or "open").strip().lower()
    if status not in {"open", "closed"}:
        raise HTTPException(status_code=400, detail="status must be open|closed")
    return list_user_sessions(u.org_id, u.user_id, status, limit=200)


@router.get("/api/chats/{session_id}")
def chats_get(session_id: str, authorization: str | None = Header(default=None)) -> dict:
    u = require_user(bearer_token(authorization))
    s = get_session(u.org_id, u.user_id, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Chat not found")
    return s


@router.get("/api/chats/{session_id}/messages")
def chats_messages(session_id: str, authorization: str | None = Header(default=None)) -> list[dict]:
    u = require_user(bearer_token(authorization))
    msgs = list_session_messages(u.org_id, u.user_id, session_id, limit=1000)
    if msgs == []:
        # Could be empty or not found; check ownership explicitly.
        s = get_session(u.org_id, u.user_id, session_id)
        if not s:
            raise HTTPException(status_code=404, detail="Chat not found")
    return msgs


@router.post("/api/chats/{session_id}/close")
def chats_close(session_id: str, authorization: str | None = Header(default=None)) -> dict:
    u = require_user(bearer_token(authorization))
    s = get_session(u.org_id, u.user_id, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Chat not found")
    close_session(session_id)

    # Clear any pending actions
    try:
        state = load_session(session_id)
        state.collected.pop("_pending_action", None)
        state.status = "closed"
        save_session(state)
    except Exception:
        pass

    return {"status": "ok"}


@router.get("/api/tickets")
def tickets_list(status: str = "created", authorization: str | None = Header(default=None)) -> list[dict]:
    u = require_user(bearer_token(authorization))
    status = (status or "created").strip().lower()
    if status not in {"created", "closed"}:
        raise HTTPException(status_code=400, detail="status must be created|closed")
    return list_user_tickets(u.org_id, u.user_id, status, limit=200)


@router.get("/api/tickets/{ticket_id}")
def tickets_get(ticket_id: str, authorization: str | None = Header(default=None)) -> dict:
    u = require_user(bearer_token(authorization))
    t = get_ticket(u.org_id, u.user_id, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    chats = list_ticket_sessions(u.org_id, u.user_id, ticket_id)
    t["chats"] = chats
    return t


@router.post("/api/chats/{session_id}/escalate")
def chats_escalate(session_id: str, payload: dict = Body(default_factory=dict), authorization: str | None = Header(default=None)) -> dict:
    """Create a ticket from a chat session and associate them."""
    u = require_user(bearer_token(authorization))
    s = get_session(u.org_id, u.user_id, session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Pull a draft from session state
    state = load_session(session_id)
    summary = str(payload.get("summary") or state.title or state.collected.get("summary") or "Issue").strip()[:120]
    category = str(payload.get("category") or state.category or "unknown").strip() or "unknown"
    reason = str(payload.get("reason") or "User requested escalation").strip() or "User requested escalation"

    ticket = Ticket(
        summary=summary,
        category=category,
        user={"org_id": u.org_id, "user_id": u.user_id},
        device={},
        diagnostics=state.collected,
        steps_attempted=state.steps_attempted,
        error_text=str(state.collected.get("error_message") or "") or None,
        escalation_reason=reason,
        citations=[],
    )
    rendered = _render_ticket(ticket)
    ticket_id = insert_ticket(
        org_id=u.org_id,
        user_id=u.user_id,
        session_id=session_id,
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
    link_session_to_ticket(session_id, ticket_id)

    # Clear pending action
    state.ticket_id = ticket_id
    state.collected.pop("_pending_action", None)
    save_session(state)

    return {"status": "ok", "ticket_id": ticket_id, "rendered": rendered}
