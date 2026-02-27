from __future__ import annotations

"""Main FastAPI app assembly.

All route handlers live in app/api/* and are included here.
Keep this module focused on:
  - app creation
  - middleware
  - startup/shutdown hooks
  - mounting static UI
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.bootstrap import router as bootstrap_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.core.auth import set_user_password
from app.core.config import settings
from app.core.db import init_schema
from app.core.repository import ensure_user
from app.rag.ingest import ensure_kb_fresh


app = FastAPI(title=settings.app_name)


def _cors_origins() -> list[str]:
    # Comma-separated list; allow JSON-ish list too.
    raw = (settings.cors_origins or "").strip()
    if not raw:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        # Best-effort parse: ["a","b"]
        raw = raw.strip("[]")
        parts = [p.strip().strip('"').strip("'") for p in raw.split(",")]
        return [p for p in parts if p]
    return [p.strip() for p in raw.split(",") if p.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=bool(getattr(settings, "cors_allow_credentials", True)),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(bootstrap_router)
app.include_router(admin_router)
app.include_router(chat_router)


@app.on_event("startup")
async def _startup() -> None:
    # Create/upgrade schema
    init_schema()

    org_id = (getattr(settings, "default_org_id", "ACME") or "ACME").strip() or "ACME"

    # Optional demo seeding (OFF by default). Enable with:
    #   TIER1_DEMO_SEED=true
    if bool(getattr(settings, "demo_seed", False)):
        ensure_user(org_id=org_id, user_id="john.doe@acme.com", first_name="John", last_name="Doe", email="john.doe@acme.com", role="end_user")
        ensure_user(org_id=org_id, user_id="jane.doe@acme.com", first_name="Jane", last_name="Doe", email="jane.doe@acme.com", role="end_user")
        ensure_user(org_id=org_id, user_id="admin.doe@acme.com", first_name="Admin", last_name="Doe", email="admin.doe@acme.com", role="admin")
        for uid in ["john.doe@acme.com", "jane.doe@acme.com", "admin.doe@acme.com"]:
            set_user_password(user_id=uid, password="Passw0rd!")

    # Keep KB + vectors in sync automatically.
    await ensure_kb_fresh(Path(settings.kb_dir), org_id=org_id)


# ---------------------------
# Static web UI (optional)
# ---------------------------
_WEB_DIR = Path(__file__).resolve().parents[1] / "web"
if _WEB_DIR.exists():
    # Mount LAST so API routes take precedence; serves index.html at /
    app.mount("/", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")