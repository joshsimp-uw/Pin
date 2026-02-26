from __future__ import annotations

import json
from typing import Any

from app.core.crypto import decrypt_str, encrypt_str
from app.core.db import connect


def get_setting(org_id: str, key: str) -> Any | None:
    conn = connect()
    try:
        row = conn.execute(
            "SELECT value_json FROM app_settings WHERE org_id=? AND key=?", (org_id, key)
        ).fetchone()
        if not row:
            return None
        return json.loads(row["value_json"])
    finally:
        conn.close()


def set_setting(org_id: str, key: str, value: Any) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO app_settings(org_id, key, value_json, updated_at)
            VALUES(?,?,?, datetime('now'))
            ON CONFLICT(org_id, key) DO UPDATE SET
              value_json=excluded.value_json,
              updated_at=datetime('now')
            """,
            (org_id, key, json.dumps(value)),
        )
        conn.commit()
    finally:
        conn.close()


def upsert_llm_provider(
    *,
    org_id: str,
    provider: str,
    model: str,
    api_key_plain: str | None = None,
) -> None:
    api_key_enc: str | None = encrypt_str(api_key_plain) if api_key_plain else None
    conn = connect()
    try:
        if api_key_enc is None:
            conn.execute(
                """
                INSERT INTO llm_providers(org_id, provider, model, api_key_enc, updated_at)
                VALUES(?,?,?,?, datetime('now'))
                ON CONFLICT(org_id, provider) DO UPDATE SET
                  model=excluded.model,
                  updated_at=datetime('now')
                """,
                (org_id, provider, model, None),
            )
        else:
            conn.execute(
                """
                INSERT INTO llm_providers(org_id, provider, model, api_key_enc, updated_at)
                VALUES(?,?,?,?, datetime('now'))
                ON CONFLICT(org_id, provider) DO UPDATE SET
                  model=excluded.model,
                  api_key_enc=excluded.api_key_enc,
                  updated_at=datetime('now')
                """,
                (org_id, provider, model, api_key_enc),
            )
        conn.commit()
    finally:
        conn.close()


def list_llm_providers(org_id: str) -> list[dict[str, Any]]:
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT provider, model, api_key_enc, updated_at FROM llm_providers WHERE org_id=? ORDER BY provider",
            (org_id,),
        ).fetchall()
        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "provider": r["provider"],
                    "model": r["model"],
                    "has_key": bool(r["api_key_enc"]),
                    "updated_at": r["updated_at"],
                }
            )
        return out
    finally:
        conn.close()


def get_llm_provider_config(org_id: str, provider: str) -> dict[str, Any] | None:
    conn = connect()
    try:
        r = conn.execute(
            "SELECT provider, model, api_key_enc FROM llm_providers WHERE org_id=? AND provider=?",
            (org_id, provider),
        ).fetchone()
        if not r:
            return None
        api_key = decrypt_str(r["api_key_enc"]) if r["api_key_enc"] else None
        return {"provider": r["provider"], "model": r["model"], "api_key": api_key}
    finally:
        conn.close()
