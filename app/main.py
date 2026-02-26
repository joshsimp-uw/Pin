from __future__ import annotations

import re
from typing import Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header
from fastapi import Body
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.db import init_schema, connect
from app.core.repository import ensure_org, ensure_user, insert_message, insert_ticket
from app.core.session import SessionState, load_session, new_session, save_session
from app.core.auth import (
    get_user_by_email,
    issue_token,
    require_admin,
    require_user,
    set_user_password,
    verify_user_password,
)
from app.core.config_store import list_llm_providers, set_setting, upsert_llm_provider, get_setting
from app.flows.engine import question_for, registry, next_missing_field
from app.llm.providers import LLMError, get_llm
from app.models.schemas import AnswerResponse, ChatRequest, ChatResponse, Ticket, TicketResponse
from app.policies.guardrails import check_response, should_escalate
from app.rag.index import retrieve
from app.rag.ingest import ingest_kb_dir, ensure_kb_fresh
from app.llm.embeddings import get_active_rag_backend, set_active_rag_backend
from app.knowledge.support import is_supported_request
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


def _bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip() or None
    return None


@app.on_event("startup")
async def _startup() -> None:
    # Create/upgrade schema for this org site's SQLite database.
    init_schema()

    # Seed demo org + users (idempotent). These are required for the capstone demo.
    demo_org = "ACME"
    ensure_org(demo_org, name="ACME")
    # User IDs are emails for simplicity.
    ensure_user(org_id=demo_org, user_id="john.doe@acme.com", first_name="John", last_name="Doe", email="john.doe@acme.com", role="end_user")
    ensure_user(org_id=demo_org, user_id="jane.doe@acme.com", first_name="Jane", last_name="Doe", email="jane.doe@acme.com", role="end_user")
    ensure_user(org_id=demo_org, user_id="admin.doe@acme.com", first_name="Admin", last_name="Doe", email="admin.doe@acme.com", role="admin")
    # Set/update their passwords.
    for uid in ["john.doe@acme.com", "jane.doe@acme.com", "admin.doe@acme.com"]:
        set_user_password(user_id=uid, password="Passw0rd!")

    # Keep KB + vectors in sync automatically.
    # - If KB files change, re-ingest.
    # - If RAG backend changes, rebuild vectors for the active backend.
    await ensure_kb_fresh(Path(settings.kb_dir), org_id=demo_org)


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
async def admin_kb_reingest(
    x_admin_token: str | None = Header(default=None),
    org_id: str = "ACME",
) -> dict[str, int]:
    """Re-ingest KB files from settings.kb_dir into SQLite + sqlite-vec.

    Provide the token via `X-Admin-Token`.
    """
    _require_admin(x_admin_token)
    stats = await ingest_kb_dir(Path(settings.kb_dir), org_id=org_id)
    return stats


@app.get("/api/admin/rag")
def admin_rag_get(authorization: str | None = Header(default=None)) -> dict:
    u = require_admin(_bearer(authorization))
    backend = get_active_rag_backend(u.org_id)
    # For UI: can we use Gemini embeddings?
    from app.core.config_store import get_llm_provider_config

    gem_cfg = get_llm_provider_config(u.org_id, "gemini") or {}
    return {
        "active": {"backend": backend},
        "available": {
            "local": True,
            "gemini": bool(gem_cfg.get("api_key") or settings.gemini_api_key),
        },
    }


@app.put("/api/admin/rag")
async def admin_rag_put(authorization: str | None = Header(default=None), payload: dict = Body(...)) -> dict:
    u = require_admin(_bearer(authorization))
    backend = str(payload.get("backend") or "local").strip().lower()
    if backend not in {"local", "gemini"}:
        raise HTTPException(status_code=400, detail="Unsupported RAG backend")
    set_active_rag_backend(u.org_id, backend)
    # Immediately rebuild embeddings for the newly-selected backend.
    await ensure_kb_fresh(Path(settings.kb_dir), org_id=u.org_id)
    return {"status": "ok", "active": {"backend": get_active_rag_backend(u.org_id)}}


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


# ===========================
# Auth + Bootstrap + Admin UI
# ===========================


@app.get("/api/bootstrap/status")
def bootstrap_status(org_id: str = "ACME") -> dict[str, bool]:
    """Return whether the org DB has been initialized via the setup page."""
    ensure_org(org_id, name=org_id)
    initialized = bool(get_setting(org_id, "initialized"))
    # Also treat "initialized" as true if there is any admin user.
    conn = connect()
    try:
        row = conn.execute("SELECT 1 FROM users WHERE org_id=? AND role='admin' LIMIT 1", (org_id,)).fetchone()
        if row:
            initialized = True
    finally:
        conn.close()
    return {"initialized": initialized}


@app.post("/api/bootstrap/setup")
def bootstrap_setup(payload: dict = Body(...)) -> dict[str, str]:
    """One-time setup for a new DB: create an admin user and initial LLM config."""
    org_id = str(payload.get("org_id") or "ACME").strip() or "ACME"
    org_name = str(payload.get("org_name") or org_id).strip() or org_id
    admin_email = str(payload.get("admin_email") or "").strip()
    admin_first = str(payload.get("admin_first") or "Admin").strip() or "Admin"
    admin_last = str(payload.get("admin_last") or "").strip() or None
    password = str(payload.get("password") or "").strip()
    llm_provider = str(payload.get("llm_provider") or "mock").strip().lower()
    llm_model = str(payload.get("llm_model") or "").strip() or ("gpt-4o-mini" if llm_provider == "openai" else "gemini-1.5-flash")
    llm_api_key = str(payload.get("llm_api_key") or "").strip() or None

    if not admin_email or not password:
        raise HTTPException(status_code=400, detail="admin_email and password are required")

    # Abort if already initialized.
    if get_setting(org_id, "initialized"):
        raise HTTPException(status_code=409, detail="Already initialized")

    ensure_org(org_id, name=org_name)
    ensure_user(
        org_id=org_id,
        user_id=admin_email,
        first_name=admin_first,
        last_name=admin_last,
        email=admin_email,
        role="admin",
    )
    set_user_password(user_id=admin_email, password=password)

    # Ensure LLM provider rows exist; store key encrypted if provided.
    if llm_provider not in {"mock", "openai", "gemini"}:
        llm_provider = "mock"
    upsert_llm_provider(org_id=org_id, provider=llm_provider, model=llm_model, api_key_plain=llm_api_key)
    set_setting(org_id, "active_llm", {"provider": llm_provider})
    set_setting(org_id, "initialized", True)
    return {"status": "ok"}


@app.post("/auth/login")
def auth_login(payload: dict = Body(...)) -> dict:
    org_id = str(payload.get("org_id") or "ACME").strip() or "ACME"
    email = str(payload.get("email") or "").strip()
    password = str(payload.get("password") or "").strip()
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password are required")
    ensure_org(org_id, name=org_id)

    u = get_user_by_email(org_id=org_id, email=email)
    if not u:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_user_password(user_id=u.user_id, password=password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = issue_token(org_id=org_id, user_id=u.user_id)
    return {
        "token": token,
        "user": {
            "user_id": u.user_id,
            "org_id": u.org_id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": u.role,
        },
    }


@app.get("/auth/me")
def auth_me(authorization: str | None = Header(default=None)) -> dict:
    u = require_user(_bearer(authorization))
    return {
        "user": {
            "user_id": u.user_id,
            "org_id": u.org_id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": u.role,
        }
    }


@app.get("/api/admin/llm")
def admin_llm_get(authorization: str | None = Header(default=None)) -> dict:
    u = require_admin(_bearer(authorization))
    ensure_org(u.org_id, name=u.org_id)
    active = get_setting(u.org_id, "active_llm") or {"provider": "mock"}
    providers = list_llm_providers(u.org_id)
    # Ensure at least the known providers exist in the list.
    known_defaults = {
        "mock": "mock",
        "openai": "gpt-4o-mini",
        "gemini": "gemini-1.5-flash",
    }
    have = {p["provider"] for p in providers}
    for prov, model in known_defaults.items():
        if prov not in have:
            upsert_llm_provider(org_id=u.org_id, provider=prov, model=model, api_key_plain=None)
    providers = list_llm_providers(u.org_id)
    return {"active": active, "providers": providers}


@app.put("/api/admin/llm")
def admin_llm_put(authorization: str | None = Header(default=None), payload: dict = Body(...)) -> dict:
    u = require_admin(_bearer(authorization))
    provider = str(payload.get("provider") or "mock").strip().lower()
    model = str(payload.get("model") or "").strip()
    api_key = str(payload.get("api_key") or "").strip() or None
    set_active = bool(payload.get("set_active", True))

    if provider not in {"mock", "openai", "gemini"}:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    if not model:
        model = "mock" if provider == "mock" else ("gpt-4o-mini" if provider == "openai" else "gemini-1.5-flash")

    upsert_llm_provider(org_id=u.org_id, provider=provider, model=model, api_key_plain=api_key)
    if set_active:
        set_setting(u.org_id, "active_llm", {"provider": provider})
    return {"status": "ok"}


@app.post("/session/new")
def create_session(authorization: str | None = Header(default=None)) -> dict[str, str]:
    """Create a new chat session for the authenticated user."""
    u = require_user(_bearer(authorization))
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


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, authorization: str | None = Header(default=None)):
    """Chat with the assistant.

    Org/user are derived from the authenticated session (Bearer token). This prevents
    callers from spoofing org_id/user_id and ensures RAG + LLM settings resolve
    against the correct org configuration from the admin portal.
    """
    u = require_user(_bearer(authorization))

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
            user={"org_id": u.org_id, "user_id": u.user_id, **{k: v for k, v in req.context.items() if k.startswith("user_")}},
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
        insert_message(session_id=state.session_id, role='assistant', content=rendered)
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
            user={"org_id": u.org_id, "user_id": u.user_id, **{k: v for k, v in req.context.items() if k.startswith("user_")}},
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

    llm = get_llm(org_id=u.org_id)
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

