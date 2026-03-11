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
        
        # 1. Identity & Access (Duo MFA)
        if any(k in m for k in ["duo", "mfa", "authenticator", "push", "token", "two factor", "2fa"]):
            return "duo_authentication"
            
        # 2. Network & Connectivity (Cisco VPN)
        if any(k in m for k in ["vpn", "cisco", "anyconnect", "pulse", "tunnel"]):
            return "vpn_connectivity"
            
        # 3. Mobile Endpoints (iOS/iPadOS)
        if any(k in m for k in ["ios", "ipad", "iphone", "mobile", "smartphone", "apple"]):
            return "mobile_endpoints"
            
        # 4. Windows Endpoints (PC/Laptop/Desktop)
        if any(k in m for k in ["windows", "pc", "laptop", "desktop", "blue screen", "boot", "surface"]):
            return "windows_endpoints"
            
        # 5. Printers & Hardware
        if any(k in m for k in ["print", "printer", "laserjet", "ink", "paper", "spooler", "toner"]):
            return "printers"
            
        # 6. SaaS & Collaboration - Zoom
        if any(k in m for k in ["zoom", "meeting", "webcam", "screen share", "screenshare", "waiting room"]):
            return "zoom_meetings"
            
        # 7. SaaS & Collaboration - SharePoint & OneDrive
        if any(k in m for k in ["sharepoint", "onedrive", "sync", "check out", "checkout", "site owner"]):
            return "sharepoint_onedrive"
            
        # 8. SaaS & Collaboration - Salesforce CRM
        if any(k in m for k in ["salesforce", "crm", "sfdc", "lead", "dashboard", "opportunity"]):
            return "salesforce_crm"
            
        # 9. Messaging - Outlook & Exchange
        if any(k in m for k in ["outlook", "email", "mailbox", "owa", "exchange", "bounce"]):
            return "messaging"
            
        # 10. Fallback
        return "fallback"

    def get(self, key: str) -> Flow:
        return self._flows.get(key) or self._fallback  # type: ignore[return-value]


registry = FlowRegistry(settings.flow_config_path)


def next_missing_field(flow: Flow, collected: dict[str, Any]) -> str | None:
    for f in flow.required_fields:
        v = collected.get(f)
        # Check for None, empty strings, or string placeholders like "null"/"unknown"
        if v is None:
            return f
        if isinstance(v, str):
            val = v.strip().lower()
            if val == "" or val == "null" or val == "unknown":
                return f
    return None


def question_for(flow: Flow, field: str) -> str:
    return flow.questions.get(field, f"Please provide: {field}")
