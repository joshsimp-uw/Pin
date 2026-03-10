from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings
from app.core.config_store import get_llm_provider_config, get_setting


class LLMError(RuntimeError):
    pass


class BaseLLM:
    async def chat(self, messages: list[dict[str, Any]], *, response_format: dict[str, Any] | None = None) -> str:
        raise NotImplementedError


class MockLLM(BaseLLM):
    async def chat(self, messages: list[dict[str, Any]], *, response_format: dict[str, Any] | None = None) -> str:
        # For offline/dev runs. Produces something deterministic.
        user_text = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_text = str(m.get("content", ""))
                break
        return f"(MOCK) I can help. Based on what you said: {user_text}\n\nIf I don't have enough documented steps, I'll escalate to a ticket."


class OpenAICompatibleLLM(BaseLLM):
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"

    async def chat(self, messages: list[dict[str, Any]], *, response_format: dict[str, Any] | None = None) -> str:
        url = self.base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        # Some OpenAI-compatible endpoints support JSON schema via response_format; optional.
        if response_format is not None:
            payload["response_format"] = response_format

        timeout = httpx.Timeout(settings.llm_timeout_s)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                r = await client.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as e:
            raise LLMError(f"LLM request timed out after {settings.llm_timeout_s:.0f}s") from e
        except httpx.HTTPError as e:
            raise LLMError(f"LLM request failed: {e}") from e

        if r.status_code >= 400:
            raise LLMError(f"LLM call failed: {r.status_code} {r.text[:500]}")

        data = r.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMError(f"Unexpected LLM response format: {json.dumps(data)[:800]}") from e


def get_llm(*, org_id: str = "demo-org") -> BaseLLM:
    """Return the active LLM.

    Preference order:
      1) Per-org DB config (admin UI / bootstrap)
      2) Environment settings (TIER1_*)
      3) Mock
    """
    active = get_setting(org_id, "active_llm")
    provider = (
        str(active.get("provider"))
        if isinstance(active, dict) and active.get("provider")
        else settings.llm_provider
    ).lower()

    db_cfg = get_llm_provider_config(org_id, provider)

    if provider == "openai":
        api_key = (db_cfg or {}).get("api_key") or settings.openai_api_key
        model = (db_cfg or {}).get("model") or settings.openai_model
        if not api_key:
            raise LLMError("OpenAI API key is not configured")
        return OpenAICompatibleLLM(
            api_key=api_key,
            model=model,
            base_url=settings.openai_base_url,
        )

    if provider == "gemini":
        from app.llm.gemini import GeminiLLM

        api_key = (db_cfg or {}).get("api_key") or settings.gemini_api_key
        model = (db_cfg or {}).get("model") or settings.gemini_model
        if not api_key:
            raise LLMError("Gemini API key is not configured")
        return GeminiLLM(api_key=api_key, model=model)

    # Mock is always available
    return MockLLM()
