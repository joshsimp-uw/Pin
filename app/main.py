from __future__ import annotations

import re
from typing import Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.db import init_schema
from app.core.repository import ensure_org, ensure_user, insert_message, insert_ticket
from app.core.session import SessionState, load_session, new_session, save_session
from app.flows.engine import question_for, registry, next_missing_field
from app.llm.providers import LLMError, get_llm
from app.models.schemas import AnswerResponse, ChatRequest, ChatResponse, Ticket, TicketResponse
from app.policies.guardrails import check_response, should_escalate
from app.rag.index import retrieve
from app.rag.ingest import ingest_kb_dir
from app.rag.vec_store import connect_vec
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # or whichever origin serves app.html
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _require_admin(x_admin_token: str | None) -> None:
    if not settings.admin_token:
        raise HTTPException(status_code=500, detail="Admin token is not configured on the server")
    if not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")


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


def _heuristic_field_guess(message: str, required_fields: list[str] | None = None) -> dict[str, Any]:
    """
    Heuristically infer answers to flow questions from natural language.
    Returns only fields we can confidently extract.
    If required_fields is provided, we limit inference to those names to avoid extra noise.
    """

    text = message.strip()
    t = text.lower()
    wants:  set[str] | None = set(required_fields) if required_fields else None
    out: dict[str, Any] = {}

    def need(name: str) -> bool:
        return True if wants is None else (name in wants)

    # ---------------------------
    # Common helpers
    # ---------------------------
    YES = {"yes", "y", "yeah", "yep", "works", "working", "ok", "okay", "fine", "success"}
    NO = {"no", "n", "nope", "not", "doesnt", "doesn't", "cant", "can't", "cannot", "broken", "fails", "failing", "failed", "error"}
    UNSURE = {"unsure", "maybe", "not sure", "unknown", "don't know", "dont know", "idk"}

    def norm_yes_no(txt: str) -> str | None:
        w = txt.lower()
        if any(wd in w for wd in YES): return "yes"
        if any(wd in w for wd in NO): return "no"
        if any(wd in w for wd in UNSURE): return "unsure"
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
        if re.search(r"\bwin(dows)?\s*11\b", t): out.setdefault("os", "Windows 11")
        elif re.search(r"\bwin(dows)?\s*10\b", t): out.setdefault("os", "Windows 10")
        elif "windows" in t: out.setdefault("os", "Windows")
        elif any(k in t for k in ["macos", "os x", "osx", "mac"]): out.setdefault("os", "macOS")
        elif any(k in t for k in ["ubuntu", "debian", "mint", "linux"]): out.setdefault("os", "Linux")
        elif any(k in t for k in ["iphone", "ipad", "ios"]): out.setdefault("os", "iOS")
        elif "android" in t: out.setdefault("os", "Android")

    # ---------------------------
    # device_type  (fallback, vpn, wifi)
    # ---------------------------
    if need("device_type"):
        if any(k in t for k in ["laptop", "notebook", "macbook", "thinkpad"]): out.setdefault("device_type", "laptop")
        elif any(k in t for k in ["desktop", "workstation", "tower"]): out.setdefault("device_type", "desktop")
        elif any(k in t for k in ["phone", "mobile", "cell", "iphone", "android"]): out.setdefault("device_type", "phone")
        elif any(k in t for k in ["ipad", "tablet"]): out.setdefault("device_type", "tablet")

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
        m = re.search(r'\berror(?:\s*code)?\s*[:#]?\s*([A-Za-z0-9._-]{2,})', text, flags=re.I)
        if m:
            out.setdefault("error_message", m.group(0).strip())
        else:
            # Common phrasing like "No Internet", "Connected without Internet"
            m2 = re.search(r'\b(no internet|connected without internet|authentication failed|timed out)\b', t, flags=re.I)
            if m2:
                out.setdefault("error_message", m2.group(0))
            else:
                m3 = re.search(r'\b\d{3,5}\b', text)  # numeric error code alone
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
        if any(k in t for k in ["outlook desktop", "outlook app"]): out.setdefault("client", "Outlook")
        elif any(k in t for k in ["outlook", "owa", "webmail", "browser"]): out.setdefault("client", "OWA")
        elif any(k in t for k in ["apple mail", "mail.app", "mail app"]): out.setdefault("client", "Apple Mail")
        elif any(k in t for k in ["gmail app", "android mail", "iphone mail", "ios mail", "mobile app"]): out.setdefault("client", "mobile app")

    # ---------------------------
    # symptom  (email)
    # ---------------------------
    if need("symptom"):
        if any(k in t for k in ["can't sign in", "cant sign in", "signin", "sign in", "login", "log in", "auth"]):
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
        if any(k in t for k in ["home", "house", "apartment"]):
            out.setdefault("location", "home")
        elif any(k in t for k in ["office", "onsite", "on-site", "campus", "building"]):
            out.setdefault("location", "office")
        elif "campus" in t:
            out.setdefault("location", "campus")

    # ---------------------------
    # other_devices  (wifi)
    # ---------------------------
    if need("other_devices"):
        v = norm_yes_no(t)
        if v:
            out.setdefault("other_devices", v)

    return out

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


@app.post("/admin/kb/reingest")
async def admin_kb_reingest(x_admin_token: str | None = Header(default=None)) -> dict[str, int]:
    """Re-ingest KB files from settings.kb_dir into SQLite + sqlite-vec.

    Provide the token via `X-Admin-Token`.
    """
    _require_admin(x_admin_token)
    stats = await ingest_kb_dir(Path(settings.kb_dir))
    return stats


@app.get("/admin/kb/docs")
def admin_kb_docs(x_admin_token: str | None = Header(default=None)) -> list[dict[str, str]]:
    """List KB documents stored in the DB."""
    _require_admin(x_admin_token)
    conn = connect_vec()
    try:
        rows = conn.execute(
            "SELECT doc_id, category, title, source_path, updated_at FROM kb_documents ORDER BY category, title"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


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

    # Retrieve docs based on message + collected context
    query = req.message + "\n" + "\n".join([f"{k}: {v}" for k, v in sorted(state.collected.items())])
    citations, best_score = await retrieve(query)

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


# ---------------------------
# Static web UI (optional)
# ---------------------------
_WEB_DIR = Path(__file__).resolve().parents[1] / "web"
if _WEB_DIR.exists():
    # Mount LAST so API routes take precedence; serves index.html at /
    app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")

