from __future__ import annotations

import base64
from pathlib import Path

from cryptography.fernet import Fernet

from app.core.config import settings


def _load_or_create_key() -> bytes:
    """Return a stable Fernet key.

    Precedence:
      1) TIER1_SECRET_KEY (expects a urlsafe base64-encoded 32-byte key)
      2) settings.secret_key_path on disk (created if missing)
    """
    if settings.secret_key:
        # Validate-ish: Fernet expects urlsafe_b64
        return settings.secret_key.encode("utf-8")

    path = Path(settings.secret_key_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path.read_bytes().strip()

    key = Fernet.generate_key()
    path.write_bytes(key)
    return key


def get_fernet() -> Fernet:
    return Fernet(_load_or_create_key())


def encrypt_str(plaintext: str) -> str:
    """Encrypt a string and return a utf-8 token."""
    f = get_fernet()
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_str(token: str) -> str:
    f = get_fernet()
    pt = f.decrypt(token.encode("utf-8"))
    return pt.decode("utf-8")
