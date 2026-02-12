from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings
from app.llm.providers import BaseLLM, LLMError


class GeminiLLM(BaseLLM):
    """Minimal Gemini wrapper using the Generative Language API (v1beta).

    We use httpx directly to avoid pulling in a heavier SDK.

    Env vars (via Settings):
      - TIER1_GEMINI_API_KEY
      - TIER1_GEMINI_MODEL (default: gemini-1.5-flash)
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def chat(self, messages: list[dict[str, Any]], *, response_format: dict[str, Any] | None = None) -> str:
        # Gemini expects "contents" with parts.
        contents: list[dict[str, Any]] = []
        for m in messages:
            role = m.get("role")
            # Gemini uses "user" and "model" roles.
            gem_role = "user" if role in ("user", "system") else "model"
            text = str(m.get("content", ""))
            contents.append({"role": gem_role, "parts": [{"text": text}]})

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
            },
        }

        timeout = httpx.Timeout(settings.llm_timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(url, json=payload)

        if r.status_code >= 400:
            raise LLMError(f"Gemini call failed: {r.status_code} {r.text[:500]}")

        data = r.json()
        try:
            # candidates[0].content.parts[0].text
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise LLMError(f"Unexpected Gemini response format: {json.dumps(data)[:800]}") from e


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings with Gemini's embedding endpoint.

    Returns a list of float vectors.
    """

    if not settings.gemini_api_key:
        raise LLMError("TIER1_GEMINI_API_KEY is required for embeddings")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_embed_model}:embedContent"
        f"?key={settings.gemini_api_key}"
    )

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
                out.append(list(data["embedding"]["values"]))
            except Exception as e:
                raise LLMError(f"Unexpected Gemini embed response: {json.dumps(data)[:800]}") from e
    return out
