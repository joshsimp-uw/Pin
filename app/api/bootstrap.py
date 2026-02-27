from __future__ import annotations

from fastapi import APIRouter, Body, Header, HTTPException

from app.api.deps import require_admin_token
from app.core.config import settings
from app.core.config_store import get_setting, set_setting, upsert_llm_provider
from app.core.db import connect
from app.core.repository import ensure_org, ensure_user
from app.core.auth import set_user_password

router = APIRouter(tags=["bootstrap"])


def _org_exists(org_id: str) -> bool:
    conn = connect()
    try:
        row = conn.execute("SELECT 1 FROM orgs WHERE org_id=? LIMIT 1", (org_id,)).fetchone()
        return bool(row)
    finally:
        conn.close()


@router.get("/api/bootstrap/status")
def bootstrap_status(org_id: str = "ACME") -> dict[str, bool]:
    """Return whether the org DB has been initialized via the setup page."""
    # Do not auto-create orgs here; missing org means not initialized.
    if not _org_exists(org_id):
        return {"initialized": False}
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


@router.post("/api/bootstrap/setup")
def bootstrap_setup(
    payload: dict = Body(...),
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> dict[str, str]:
    """One-time setup for a new DB: create an admin user and initial LLM config."""
    org_id = str(payload.get("org_id") or "ACME").strip() or "ACME"
    org_name = str(payload.get("org_name") or org_id).strip() or org_id
    admin_email = str(payload.get("admin_email") or "").strip()
    admin_first = str(payload.get("admin_first") or "Admin").strip() or "Admin"
    admin_last = str(payload.get("admin_last") or "").strip() or None
    password = str(payload.get("password") or "").strip()
    llm_provider = str(payload.get("llm_provider") or "mock").strip().lower()
    llm_model = str(payload.get("llm_model") or "").strip() or (
        "gpt-4o-mini" if llm_provider == "openai" else "gemini-1.5-flash"
    )
    llm_api_key = str(payload.get("llm_api_key") or "").strip() or None

    if not bool(getattr(settings, "bootstrap_enabled", True)):
        raise HTTPException(status_code=404, detail="Bootstrap is disabled on this server")

    # In non-dev environments, require the server's admin token to run bootstrap.
    if str(getattr(settings, "environment", "dev")).lower() != "dev":
        require_admin_token(x_admin_token)

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
