# Security / Safety Notes (MVP)

This is a capstone-style MVP. If you deploy it for real, tighten these areas.

## Data handling
- Do **not** log secrets (tokens, passwords, cookies, API keys).
- Redact or hash identifiers where possible.
- Treat chat logs as sensitive (they may contain PII).

## Guardrails
Implemented:
- Banned phrase blocklist (very basic)
- Escalation on low documentation confidence

Recommended upgrades:
- Output schema validation + tool-failure fallbacks
- Security policy checks by category (e.g., identity, endpoint protection)
- Admin-only procedures gated by role

## Access control
- Add OIDC/SAML and pass org/user context to the assistant
- Partition KB and sessions per org

## Prompt injection
- Never trust user input to override system rules
- Keep company procedures outside the model whenever possible (flow config + deterministic actions)
