from __future__ import annotations

import hashlib
import hmac
import os
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.core.config import settings
from app.core.db import connect


PBKDF2_ITERS = 210_000


def _pbkdf2_hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERS)


def set_user_password(*, user_id: str, password: str) -> None:
    salt = os.urandom(16)
    ph = _pbkdf2_hash(password, salt)
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO user_auth(user_id, password_salt, password_hash, algo, updated_at)
            VALUES(?,?,?,?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
              password_salt=excluded.password_salt,
              password_hash=excluded.password_hash,
              algo=excluded.algo,
              updated_at=datetime('now')
            """,
            (user_id, salt, ph, "pbkdf2_sha256"),
        )
        conn.commit()
    finally:
        conn.close()


def verify_user_password(*, user_id: str, password: str) -> bool:
    conn = connect()
    try:
        row = conn.execute(
            "SELECT password_salt, password_hash, algo FROM user_auth WHERE user_id=?", (user_id,)
        ).fetchone()
        if not row:
            return False
        salt = bytes(row["password_salt"]) if isinstance(row["password_salt"], (bytes, bytearray)) else row["password_salt"]
        expected = bytes(row["password_hash"]) if isinstance(row["password_hash"], (bytes, bytearray)) else row["password_hash"]
        got = _pbkdf2_hash(password, salt)
        return hmac.compare_digest(expected, got)
    finally:
        conn.close()


@dataclass(frozen=True)
class AuthUser:
    user_id: str
    org_id: str
    email: str | None
    first_name: str | None
    last_name: str | None
    role: str


def get_user_by_email(*, org_id: str, email: str) -> AuthUser | None:
    conn = connect()
    try:
        row = conn.execute(
            "SELECT user_id, org_id, email, first_name, last_name, role FROM users WHERE org_id=? AND lower(email)=lower(?)",
            (org_id, email),
        ).fetchone()
        if not row:
            return None
        return AuthUser(
            user_id=row["user_id"],
            org_id=row["org_id"],
            email=row["email"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            role=row["role"],
        )
    finally:
        conn.close()


def issue_token(*, org_id: str, user_id: str, expires_at: str | None = None) -> str:
    token = str(uuid.uuid4())

    # Default TTL unless caller explicitly provides an expiry.
    if expires_at is None:
        ttl = int(getattr(settings, "session_ttl_seconds", 0) or 0)
        if ttl > 0:
            dt = datetime.utcnow() + timedelta(seconds=ttl)
            # Match SQLite datetime('now') format (UTC) for easy comparison in SQL.
            expires_at = dt.strftime("%Y-%m-%d %H:%M:%S")

    conn = connect()
    try:
        conn.execute(
            "INSERT INTO auth_sessions(token, user_id, org_id, expires_at) VALUES(?,?,?,?)",
            (token, user_id, org_id, expires_at),
        )
        conn.commit()
        return token
    finally:
        conn.close()


def get_user_by_token(token: str) -> AuthUser | None:
    conn = connect()
    try:
        # Enforce session expiry. If expires_at is NULL, treat as non-expiring
        # (legacy behavior), otherwise require expires_at > now.
        row = conn.execute(
            """
            SELECT u.user_id, u.org_id, u.email, u.first_name, u.last_name, u.role,
                   s.expires_at AS expires_at
            FROM auth_sessions s
            JOIN users u ON u.user_id = s.user_id
            WHERE s.token=?
              AND (s.expires_at IS NULL OR s.expires_at > datetime('now'))
            """,
            (token,),
        ).fetchone()

        if not row:
            # Opportunistic cleanup of expired sessions for this token.
            conn.execute("DELETE FROM auth_sessions WHERE token=? AND expires_at IS NOT NULL AND expires_at <= datetime('now')", (token,))
            conn.commit()
            return None

        return AuthUser(
            user_id=row["user_id"],
            org_id=row["org_id"],
            email=row["email"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            role=row["role"],
        )
    finally:
        conn.close()


def require_user(token: str | None) -> AuthUser:
    if not token:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    u = get_user_by_token(token)
    if not u:
        raise HTTPException(status_code=401, detail="Invalid token")
    return u


def require_admin(token: str | None) -> AuthUser:
    u = require_user(token)
    if u.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return u
