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
import json

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


async def _merge_collected(state: SessionState, req: ChatRequest, org_id: str) -> None:
    # Helper to check if a value is effectively "missing"
    def is_empty(v):
        if v is None: return True
        if isinstance(v, str):
            sv = v.strip().lower()
            return sv == "" or sv == "null" or sv == "unknown"
        return False

    # 1) Parse explicit kv fields first (e.g., connection_type: USB)
    kv = _extract_kv(req.message)
    for k, v in kv.items():
        # Allow overwriting if the current value is empty/null
        if k not in state.collected or is_empty(state.collected.get(k)):
            state.collected[k] = v

    # 2) Identify fields that are missing or currently "null"
    flow = registry.get(state.category)
    required = list(getattr(flow, "required_fields", []) or [])
    
    # NEW LOGIC: If a field is "null", it counts as missing for the LLM extraction
    missing = [f for f in required if is_empty(state.collected.get(f))]
    
    if missing:
        guessed = await _llm_field_extract(req.message, required_fields=missing, org_id=org_id)
        for k, v in guessed.items():
            # Only save the guess if it's not empty AND we don't have a better value yet
            if not is_empty(v):
                if k not in state.collected or is_empty(state.collected.get(k)):
                    state.collected[k] = v

    # 3) Accept explicit context from client
    if req.context:
        for k, v in req.context.items():
            kk = str(k).strip().lower()
            if kk in required and not is_empty(v):
                if is_empty(state.collected.get(kk)):
                    state.collected[kk] = v


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

    # 0. GREETING INTERCEPT: Prevent simple greetings from starting a flow
    # Strip punctuation to catch "Hello!" or "hi."
    import re
    msg_clean = re.sub(r'[^a-z\s]', '', req.message.lower()).strip()
    greetings = {"hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "sup"}
    
    if not state.category and msg_clean in greetings:
        prompt = "Hello! I'm your IT support assistant. How can I help you today?"
        
        # Save the interaction to the database history
        insert_message(session_id=state.session_id, role="user", content=req.message)
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        
        # Save the session without incrementing turns or setting a category
        save_session(state)
        
        return AnswerResponse(
            message=prompt,
            citations=[],
            collected=state.collected
        )

    # Existing code continues here:
    state.turns += 1

    if not state.category:
        state.category = registry.classify(req.message)

    flow = registry.get(state.category)

    # 0.5 INPUT GUARDRAILS: Check user message for banned phrases immediately
    input_gr = check_response(req.message)
    if not input_gr.ok:
        prompt = input_gr.reason  # Outputs: "That is an unsafe request, please try again."
        
        # Wipe memory
        state.category = None
        state.collected.clear()
        
        insert_message(session_id=state.session_id, role="user", content=req.message)
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        
        return AnswerResponse(
            message=prompt,
            citations=[],
            collected=state.collected
        )

    # 1. INTENT EXTRACTION: Call the async merge function using the LLM
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

        # 2. PENDING ACTIONS: Handle confirmations (Close Chat / Escalate)
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

                return AnswerResponse(
                    message=f"Success! I've created ticket #{ticket_id} for you. Is there anything else I can help with today?", 
                    citations=[], 
                    collected=state.collected
                )
            
        if no:
            state.collected.pop("_pending_action", None)
            save_session(state)
        else:
            prompt = str(pending.get("prompt") or "Please reply yes or no.")
            insert_message(session_id=state.session_id, role="assistant", content=prompt)
            save_session(state)
            return ActionResponse(message=prompt, actions=[Action(action_id="yes", label="Yes"), Action(action_id="no", label="No")], meta={"pending": pending.get("type")})
        
    # 3. AUTO-CLOSE: Check for resolution keywords
    msg_l = req.message.strip().lower()
    if any(k in msg_l for k in ["that resolved it", "issue resolved", "matter resolved", "problem solved", "thank you", "thanks", "problem resolved", "error resolved", "problem corrected", "problem has been fixed", "problem fixed", "that fixed it"]):
        prompt = "Glad to hear it. Would you like to close this chat?"
        state.collected["_pending_action"] = {"type": "close_chat", "prompt": prompt}
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        return ActionResponse(message=prompt, actions=[Action(action_id="yes", label="Close chat"), Action(action_id="no", label="Keep open")], meta={"pending": "close_chat"})


    # 3.5 AUTO-ESCALATE: Check for failure/unresolved keywords after steps were provided
    # We check if state.turns > 1 to ensure the bot has actually provided steps first.
    if state.turns > 1 and any(k in msg_l for k in ["didn't work", "did not work", "still not working", "no luck", "failed", "didn't help", "did not help", "still broken", "same error"]):
        ticket = Ticket(
            summary=state.collected.get("summary") or state.title or req.message.strip()[:120],
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
            escalation_reason="User reported that the provided troubleshooting steps did not resolve the issue.",
            citations=[],
        )
        
        prompt = "It sounds like those steps didn't resolve the issue. Would you like me to escalate this chat to a ticket for the helpdesk?"
        
        state.collected["_pending_action"] = {
            "type": "escalate_to_ticket",
            "prompt": prompt,
            "draft": ticket.model_dump(),
        }
        
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        
        return ActionResponse(
            message=prompt, 
            actions=[
                Action(action_id="yes", label="Yes, create ticket"), 
                Action(action_id="no", label="No, I'll keep trying")
            ], 
            meta={"pending": "escalate_to_ticket"}
        )


    # 4. THE GATEKEEPER: Check for missing fields BEFORE RAG retrieval
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

# 4.5 SUPPORT MATRIX CHECK: Now uses the LLM-driven async check
    supported, unsupp_reason = await is_supported_request(
        message=req.message,
        category=state.category,
        collected=state.collected,
        kb_dir=Path(settings.kb_dir),
        org_id=u.org_id  # Pass the org_id so get_llm works
    )
    
    if not supported:
        # 1. Define the hard rejection message
        prompt = f"Sorry, this organization does not support that ({unsupp_reason}). Please try again with a supported topic."
        
        # 2. Wipe the memory so the bot forgets about the unsupported app
        # This ensures their next message starts fresh.
        state.category = None
        state.collected.clear()
        
        # 3. Save the rejection to the chat history
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        
        # 4. Return an AnswerResponse (No buttons, no tickets)
        return AnswerResponse(
            message=prompt,
            citations=[],
            collected=state.collected
        )
    
    # 5. RETRIEVAL: Only proceed to search if all fields are valid
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
        query = req.message + "\n" + "\n".join([f"{k}: {v}" for k, v in sorted(state.collected.items())])

    citations, best_score = await retrieve(query, org_id=u.org_id)

    # 6. ESCALATION: Confidence check
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

    # 7. RESPONSE GENERATION: Final troubleshooting synthesis
    system = (
        "You are a Tier 0/Tier 1 IT support technician for a single company. "
        "Stay in scope. Use ONLY the provided KB excerpts as your source of truth. "
        "Format your response using Markdown (bolding, numbered lists). "
        "Do not include source numbers like (SOURCE 1) in your text response. "
        "You MUST cite your sources, but do so sparingly. Cite each document used exactly ONE time. Even if you use multiple excerpts from the exact same document, do not repeat the citation. Place your citation at the very end of the troubleshooting section, rather than after every paragraph or step. "
        "The document titles provided to you contain multiple parts separated by dashes. "
        "When formatting your citation, you MUST extract the core issue name and append the word 'Policy' to the end of it. Ignore the broad categories at the beginning and the final section heading at the end. "
        "For example, if the provided title is 'Printers — HP LaserJet — Driver or install problems — Severity', your citation must be exactly: (Driver or install problems Policy). "
        "If the KB does not contain a clear procedure, offer to escalate."
        "ESCALATION RULES: "
        "1. If you are providing ANY troubleshooting steps for the user to try, you MUST NOT escalate. "
        "2. ONLY output the exact token ACTION_ESCALATE on a new line at the very end of your response if the user has ALREADY tried all available steps, OR if their specific symptoms perfectly match the 'Escalate if' criteria in the KB. "
        "3. Never output the token for a hypothetical future situation."
    )

    kb_block = "\n\n".join([f"SOURCE {i+1}: {c.title}\n{c.snippet}" for i, c in enumerate(citations)])
    user_prompt = (
        f"User issue:\n{req.message}\n\n"
        f"Collected context:\n" + "\n".join([f"- {k}: {v}" for k, v in sorted(state.collected.items())]) + "\n\n"
        f"KB excerpts:\n{kb_block}\n\n"
        "Respond with: (1) a short diagnosis, (2) numbered steps, (3) what to report back."
    )

    try:
        content = await llm.chat(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ]
        )
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # 7.5 POST-GENERATION INTERCEPT: Catch explicit LLM-driven escalations
    # Notice we are checking for the exact uppercase string now, not just "escalat"
    if "ACTION_ESCALATE" in content:
        
        # Optional: Clean the ugly trigger word out of the text so the user doesn't see it
        clean_content = content.replace("ACTION_ESCALATE", "").strip()
        
        ticket = Ticket(
            summary=state.collected.get("summary") or req.message.strip()[:120],
            category=state.category or "unknown",
            user={"org_id": u.org_id, "user_id": u.user_id},
            device={k: v for k, v in req.context.items() if k.startswith("device_")},
            diagnostics=state.collected,
            steps_attempted=state.steps_attempted,
            error_text=str(state.collected.get("error_message") or "") or None,
            escalation_reason="LLM determined escalation was necessary based on KB rules.",
            citations=citations,
        )
        
        # We append the LLM's explanation (clean_content) to the prompt
        prompt = f"{clean_content}\n\nWould you like me to create a ticket for you?"
        
        state.collected["_pending_action"] = {
            "type": "escalate_to_ticket",
            "prompt": prompt,
            "draft": ticket.model_dump(),
        }
        
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        
        return ActionResponse(
            message=prompt,
            actions=[
                Action(action_id="escalate", label="Escalate to ticket"), 
                Action(action_id="no", label="Keep chatting")
            ],
            meta={"pending": "escalate_to_ticket"},
        )

    # 8. GUARDRAILS: Check output safety (Active at all turns)
    gr = check_response(content)
    if not gr.ok:
        # 1. Use the exact custom message returned by the guardrail
        prompt = gr.reason
        
        # 2. Wipe the memory so the bot forgets the malicious/forbidden context
        state.category = None
        state.collected.clear()
        
        # 3. Save the rejection to the chat history
        insert_message(session_id=state.session_id, role="assistant", content=prompt)
        save_session(state)
        
        # 4. Return an AnswerResponse (No buttons, no tickets)
        return AnswerResponse(
            message=prompt,
            citations=[],
            collected=state.collected
        )

    insert_message(
        session_id=state.session_id,
        role="assistant",
        content=content,
        citations=[c.model_dump() for c in citations],
    )
    save_session(state)
    return AnswerResponse(message=content, citations=citations, collected=state.collected)
