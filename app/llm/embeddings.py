from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable

import httpx

from app.core.config import settings
from app.core.config_store import get_llm_provider_config, get_setting
from app.llm.providers import LLMError


def _normalize(v: list[float]) -> list[float]:
    # L2 normalize to make cosine distance meaningful.
    s = math.sqrt(sum(x * x for x in v))
    if s <= 0:
        return v
    return [x / s for x in v]


def _hash_embed(text: str, *, dim: int) -> list[float]:
    """Deterministic local embedding with feature hashing.

    This is intentionally lightweight (no extra model deps) so the app can run
    offline after bootstrap. It's not SOTA, but it's stable and works well
    enough for small KB prototypes.
    """

    t = re.sub(r"\s+", " ", (text or "").lower()).strip()
    if not t:
        return [0.0] * dim

    vec = [0.0] * dim
    # Mix token + char 3-grams to be resilient to typos and small phrasing changes.
    tokens = re.findall(r"[a-z0-9]+", t)
    grams: list[str] = []
    s = f" {t} "
    for i in range(max(0, len(s) - 2)):
        grams.append(s[i : i + 3])

    for feat in tokens + grams:
        h = hashlib.blake2b(feat.encode("utf-8"), digest_size=8).digest()
        idx = int.from_bytes(h[:4], "little") % dim
        sign = -1.0 if (h[4] & 1) else 1.0
        vec[idx] += sign

    return _normalize(vec)


def get_active_rag_backend(org_id: str) -> str:
    """Return active RAG backend for this org: 'local' or 'gemini'.

    Default behavior:
      - If org has a stored Gemini API key, default to 'gemini'
      - Else default to 'local'
    """
    active = get_setting(org_id, "active_rag") or {}
    backend = str(active.get("backend") or "").strip().lower()
    if backend in {"local", "gemini"}:
        return backend

    # Auto-default based on whether a Gemini key exists in the org config.
    cfg = get_llm_provider_config(org_id, "gemini")
    if cfg and cfg.get("api_key"):
        return "gemini"
    # Fallback to env if provided.
    if settings.gemini_api_key:
        return "gemini"
    return "local"


def set_active_rag_backend(org_id: str, backend: str) -> None:
    b = (backend or "local").strip().lower()
    if b not in {"local", "gemini"}:
        b = "local"
    from app.core.config_store import set_setting

    set_setting(org_id, "active_rag", {"backend": b})


def rag_embedding_dim_for_backend(backend: str) -> int:
    b = (backend or "local").strip().lower()
    return int(settings.rag_embedding_dim_gemini if b == "gemini" else settings.rag_embedding_dim_local)


async def embed_texts(texts: list[str], *, org_id: str, backend: str) -> list[list[float]]:
    b = (backend or "local").strip().lower()
    if b == "gemini":
        return await _embed_gemini(texts, org_id=org_id)
    dim = rag_embedding_dim_for_backend("local")
    return [_hash_embed(t, dim=dim) for t in texts]


async def _embed_gemini(texts: list[str], *, org_id: str) -> list[list[float]]:
    cfg = get_llm_provider_config(org_id, "gemini") or {}
    api_key = (cfg.get("api_key") or settings.gemini_api_key)
    if not api_key:
        raise LLMError("Gemini API key is required for Gemini embeddings")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_embed_model}:embedContent?key={api_key}"

    timeout = httpx.Timeout(settings.llm_timeout_s)
    out: list[list[float]] = []
    async with httpx.AsyncClient(timeout=timeout) as client:
        for t in texts:
            payload = {"content": {"parts": [{"text": t}]}}
            r = await client.post(url, json=payload)
            if r.status_code >= 400:
                raise LLMError(f"Gemini embed failed: {r.status_code} {r.text[:500]}")
            data = r.json()
            try:
                out.append(_normalize(list(data["embedding"]["values"])))
            except Exception as e:
                raise LLMError(f"Unexpected Gemini embed response: {str(data)[:800]}") from e
    return out
