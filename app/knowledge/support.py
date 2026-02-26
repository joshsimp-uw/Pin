from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("/", " ")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_\-]", "", s)
    return s


def support_matrix(kb_dir: Path) -> dict[str, dict[str, list[str]]]:
    """Return {device_type: {os: [applications...]}} based on directory structure."""
    out: dict[str, dict[str, list[str]]] = {}
    if not kb_dir.exists():
        return out
    for device in sorted([p for p in kb_dir.iterdir() if p.is_dir()]):
        if device.name.startswith((".", "_")):
            continue
        dkey = _slug(device.name)
        out[dkey] = {}
        for os_dir in sorted([p for p in device.iterdir() if p.is_dir()]):
            if os_dir.name.startswith((".", "_")):
                continue
            okey = _slug(os_dir.name)
            apps: list[str] = []
            for app_dir in sorted([p for p in os_dir.iterdir() if p.is_dir()]):
                if app_dir.name.startswith((".", "_")):
                    continue
                apps.append(_slug(app_dir.name))
            out[dkey][okey] = apps
    return out


def _guess_application(message: str, category: str) -> str | None:
    t = (message or "").lower()
    # Prefer an explicit app hint if present.
    for k, app in [
        ("outlook", "outlook"),
        ("office", "office"),
        ("word", "office"),
        ("excel", "office"),
        ("powerpoint", "office"),
        ("teams", "teams"),
        ("vpn", "vpn"),
        ("wifi", "wifi"),
        ("wi-fi", "wifi"),
        ("printer", "printers"),
        ("printing", "printers"),
    ]:
        if k in t:
            return app
    # Fall back to the classifier category (email, remote_access, printers, ...)
    return _slug(category) if category else None


def is_supported_request(
    *,
    message: str,
    category: str,
    collected: dict[str, Any],
    kb_dir: Path,
) -> tuple[bool, str | None]:
    """Return (supported, reason).

    We treat the KB folder list as the authoritative support matrix:
      knowledge/<device type>/<operating system>/<application>/<issue.md>

    If the user asks about something not present in the directory tree, we
    escalate as "unsupported".
    """

    matrix = support_matrix(kb_dir)
    if not matrix:
        # If KB isn't present, don't block; normal RAG confidence escalation will handle it.
        return True, None

    device = _slug(str(collected.get("device_type") or ""))
    os_name = _slug(str(collected.get("os") or ""))
    app = _slug(str(collected.get("application") or "") or (_guess_application(message, category) or ""))

    # Only enforce checks when we have a signal. We don't want to falsely block
    # early turns before the flow collects required fields.
    if device and device not in matrix:
        return False, f"Unsupported device type '{device}'."
    if device and os_name and os_name not in matrix.get(device, {}):
        return False, f"Unsupported OS '{os_name}' for device type '{device}'."
    if device and os_name and app:
        apps = set(matrix.get(device, {}).get(os_name, []))
        if apps and app not in apps:
            return False, f"Unsupported application '{app}' for '{device}/{os_name}'."

    return True, None
