from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings


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
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(url, headers=headers, json=payload)

        if r.status_code >= 400:
            raise LLMError(f"LLM call failed: {r.status_code} {r.text[:500]}")

        data = r.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMError(f"Unexpected LLM response format: {json.dumps(data)[:800]}") from e


def get_llm() -> BaseLLM:
    if settings.llm_provider.lower() == "openai":
        if not settings.openai_api_key:
            raise LLMError("TIER1_OPENAI_API_KEY is required when TIER1_LLM_PROVIDER=openai")
        return OpenAICompatibleLLM(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            base_url=settings.openai_base_url,
        )
    return MockLLM()
