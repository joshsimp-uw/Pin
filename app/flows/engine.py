from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from app.core.config import settings


@dataclass
class Flow:
    key: str
    description: str
    required_fields: list[str]
    questions: dict[str, str]
    max_steps: int = 6


class FlowRegistry:
    def __init__(self, path: str):
        self.path = path
        self._flows: dict[str, Flow] = {}
        self._fallback: Flow | None = None
        self._load()

    def _load(self) -> None:
        p = Path(self.path)
        if not p.exists():
            raise FileNotFoundError(f"Flow config not found: {p.resolve()}")
        data = yaml.safe_load(p.read_text(encoding="utf-8"))

        cats = data.get("categories", {})
        for key, cfg in cats.items():
            self._flows[key] = Flow(
                key=key,
                description=str(cfg.get("description", "")),
                required_fields=list(cfg.get("required_fields", [])),
                questions=dict(cfg.get("questions", {})),
                max_steps=int(cfg.get("max_steps", 6)),
            )

        fb = data.get("fallback", {})
        self._fallback = Flow(
            key="fallback",
            description=str(fb.get("description", "")),
            required_fields=list(fb.get("required_fields", [])),
            questions=dict(fb.get("questions", {})),
            max_steps=int(fb.get("max_steps", 6)),
        )

    def classify(self, message: str) -> str:
        """Cheap keyword classifier.

        Replace with an LLM classifier later if you want, but keywording is often
        enough for Tier 0/1 routing.
        """
        m = message.lower()
        if any(k in m for k in ["vpn", "pulse", "anyconnect", "tunnel"]):
            return "vpn"
        if any(k in m for k in ["outlook", "email", "mailbox", "owa", "exchange"]):
            return "email"
        if any(k in m for k in ["wifi", "wi-fi", "wireless", "ssid"]):
            return "wifi"
        return "fallback"

    def get(self, key: str) -> Flow:
        return self._flows.get(key) or self._fallback  # type: ignore[return-value]


registry = FlowRegistry(settings.flow_config_path)


def next_missing_field(flow: Flow, collected: dict[str, Any]) -> str | None:
    for f in flow.required_fields:
        v = collected.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            return f
    return None


def question_for(flow: Flow, field: str) -> str:
    return flow.questions.get(field, f"Please provide: {field}")
