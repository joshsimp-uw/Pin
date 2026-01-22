from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass
class GuardrailResult:
    ok: bool
    reason: str | None = None


BANNED_PHRASES = [
    "disable antivirus",
    "turn off mfa",
    "bypass",
    "crack",
    "steal",
    "phishing",
    "password please",
]


def check_response(text: str) -> GuardrailResult:
    t = text.lower()
    for p in BANNED_PHRASES:
        if p in t:
            return GuardrailResult(False, f"Banned phrase detected: {p}")
    if len(text) > 5000:
        return GuardrailResult(False, "Response too long")
    return GuardrailResult(True)


def should_escalate(turns: int, best_rag_score: float) -> tuple[bool, str | None]:
    if turns >= settings.max_turns_before_escalate:
        return True, f"Exceeded max turns ({settings.max_turns_before_escalate})"
    if best_rag_score < settings.rag_min_score:
        return True, "Insufficient documentation coverage (low retrieval confidence)"
    return False, None
