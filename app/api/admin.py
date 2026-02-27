from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Body, Header, HTTPException

from app.api.deps import require_admin_from_auth_header
from app.core.config import settings
from app.core.config_store import list_llm_providers, get_setting, set_setting, upsert_llm_provider
from app.core.repository import ensure_org
from app.llm.providers import get_llm, LLMError
from app.llm.embeddings import get_active_rag_backend, set_active_rag_backend
from app.rag.ingest import ingest_kb_dir, ensure_kb_fresh
from app.rag.vec_store import connect_vec

router = APIRouter(tags=["admin"])


@router.post("/admin/kb/reingest")
async def admin_kb_reingest(authorization: str | None = Header(default=None)) -> dict[str, int]:
    """Re-ingest KB files from settings.kb_dir into SQLite + sqlite-vec.

    Admin-only endpoint.
    """
    u = require_admin_from_auth_header(authorization)
    stats = await ingest_kb_dir(Path(settings.kb_dir), org_id=u.org_id)
    return stats


@router.get("/admin/kb/docs")
def admin_kb_docs(authorization: str | None = Header(default=None)) -> list[dict[str, str]]:
    """List KB documents stored in the DB (admin-only)."""
    u = require_admin_from_auth_header(authorization)
    conn = connect_vec()
    try:
        rows = conn.execute(
            "SELECT doc_id, category, title, source_path, updated_at FROM kb_documents ORDER BY category, title"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@router.get("/api/admin/rag")
def admin_rag_get(authorization: str | None = Header(default=None)) -> dict:
    u = require_admin_from_auth_header(authorization)
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


@router.put("/api/admin/rag")
async def admin_rag_put(authorization: str | None = Header(default=None), payload: dict = Body(...)) -> dict:
    u = require_admin_from_auth_header(authorization)
    backend = str(payload.get("backend") or "local").strip().lower()
    if backend not in {"local", "gemini"}:
        raise HTTPException(status_code=400, detail="Unsupported RAG backend")
    set_active_rag_backend(u.org_id, backend)
    # Immediately rebuild embeddings for the newly-selected backend.
    await ensure_kb_fresh(Path(settings.kb_dir), org_id=u.org_id)
    return {"status": "ok", "active": {"backend": get_active_rag_backend(u.org_id)}}


@router.get("/api/admin/llm")
def admin_llm_get(authorization: str | None = Header(default=None)) -> dict:
    u = require_admin_from_auth_header(authorization)
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


@router.get("/api/admin/diagnostics")
async def admin_diagnostics(authorization: str | None = Header(default=None)) -> dict:
    """Run lightweight diagnostics for LLM + RAG (admin-only).

    This endpoint is meant for debugging deployments where the chat route is
    failing (e.g., Gemini connectivity) or where it's unclear if the KB has
    been ingested.
    """
    u = require_admin_from_auth_header(authorization)

    # --- DB stats ---
    conn = connect_vec()
    try:
        docs = int(conn.execute("SELECT COUNT(*) AS n FROM kb_documents").fetchone()["n"])
        chunks = int(conn.execute("SELECT COUNT(*) AS n FROM kb_chunks").fetchone()["n"])
        # vec tables may not exist yet
        def safe_count(table: str) -> int:
            try:
                return int(conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"])
            except Exception:
                return 0

        vec_local = safe_count("kb_vec_local")
        vec_gemini = safe_count("kb_vec_gemini")
    finally:
        conn.close()

    # --- RAG backend ---
    rag_backend = get_active_rag_backend(u.org_id)

    # --- LLM ping ---
    llm_provider: str = "unknown"
    llm_ok = False
    llm_error: str | None = None
    try:
        llm = get_llm(org_id=u.org_id)
        llm_provider = llm.__class__.__name__
        _ = await llm.chat(
            [
                {"role": "system", "content": "You are a health check."},
                {"role": "user", "content": "Reply with the single word: OK"},
            ]
        )
        llm_ok = True
    except LLMError as e:
        llm_error = str(e)

    return {
        "org_id": u.org_id,
        "rag": {"active_backend": rag_backend, "kb_docs": docs, "kb_chunks": chunks, "vec_local": vec_local, "vec_gemini": vec_gemini},
        "llm": {"impl": llm_provider, "ok": llm_ok, "error": llm_error},
    }


@router.put("/api/admin/llm")
def admin_llm_put(authorization: str | None = Header(default=None), payload: dict = Body(...)) -> dict:
    u = require_admin_from_auth_header(authorization)
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
