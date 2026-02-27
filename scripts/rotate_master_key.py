#!/usr/bin/env python3
"""Rotate the master encryption key used to protect stored provider API keys.

Pin stores provider keys encrypted (llm_providers.api_key_enc). The encryption
key (KEK) should live outside the repo and be injected via systemd as
TIER1_SECRET_KEY (typically from /etc/pin/pin.env).

Rotation flow:
  1) Load old key from env file (TIER1_SECRET_KEY)
  2) Decrypt all stored secrets
  3) Generate (or accept) a new key
  4) Update env file with the new key (with a backup)
  5) Re-encrypt secrets and write them back to sqlite

Run as root on the server, then restart pin.service.
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet


ENV_KEY = "TIER1_SECRET_KEY"


def _generate_key() -> str:
    # Fernet key format: urlsafe base64-encoded 32-byte key
    return base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")


def _read_env_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Env file not found: {path}")
    return path.read_text(encoding="utf-8")


def _extract_env_value(env_text: str, key: str) -> str | None:
    # Supports: KEY=value and optional quotes
    m = re.search(rf"^\s*{re.escape(key)}\s*=\s*(.+?)\s*$", env_text, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        val = val[1:-1]
    return val


def _upsert_env_value(env_text: str, key: str, value: str) -> str:
    line = f"{key}={value}"
    if re.search(rf"^\s*{re.escape(key)}\s*=.*$", env_text, re.MULTILINE):
        return re.sub(
            rf"^\s*{re.escape(key)}\s*=.*$",
            line,
            env_text,
            flags=re.MULTILINE,
        )
    # Append with a newline
    if not env_text.endswith("\n"):
        env_text += "\n"
    return env_text + line + "\n"


def _fernet(key: str) -> Fernet:
    try:
        return Fernet(key.encode("utf-8"))
    except Exception as e:  # pragma: no cover
        raise ValueError(f"Invalid {ENV_KEY} value (must be urlsafe base64 32-byte): {e}")


@dataclass
class ProviderRow:
    org_id: str
    provider: str
    api_key_enc: str


def _load_provider_rows(conn: sqlite3.Connection) -> list[ProviderRow]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT org_id, provider, api_key_enc FROM llm_providers WHERE api_key_enc IS NOT NULL AND api_key_enc != ''"
    ).fetchall()
    return [ProviderRow(r["org_id"], r["provider"], r["api_key_enc"]) for r in rows]


def _update_provider_row(conn: sqlite3.Connection, row: ProviderRow, new_token: str) -> None:
    conn.execute(
        "UPDATE llm_providers SET api_key_enc=?, updated_at=datetime('now') WHERE org_id=? AND provider=?",
        (new_token, row.org_id, row.provider),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Rotate Pin master encryption key (TIER1_SECRET_KEY).")
    ap.add_argument("--env-file", default="/etc/pin/pin.env", help="Path to env file used by pin.service")
    ap.add_argument("--sqlite-path", default="data/pin.db", help="Path to Pin sqlite DB")
    ap.add_argument("--new-key", default=None, help="Provide a new Fernet key; if omitted, one is generated")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Decrypt/re-encrypt in memory but do not write env/db changes",
    )
    args = ap.parse_args()

    env_path = Path(args.env_file)
    db_path = Path(args.sqlite_path)
    if not db_path.exists():
        print(f"ERROR: sqlite db not found: {db_path}", file=sys.stderr)
        return 2

    env_text = _read_env_file(env_path)
    old_key = _extract_env_value(env_text, ENV_KEY)
    if not old_key:
        print(
            f"ERROR: {ENV_KEY} not found in {env_path}. Add it first (make install does this automatically).",
            file=sys.stderr,
        )
        return 2

    new_key = args.new_key or _generate_key()

    old_f = _fernet(old_key)
    new_f = _fernet(new_key)

    conn = sqlite3.connect(str(db_path))
    try:
        rows = _load_provider_rows(conn)
        if not rows:
            print("No encrypted provider keys found in llm_providers; nothing to rotate.")
            if not args.dry_run:
                # Still update env key if requested
                updated = _upsert_env_value(env_text, ENV_KEY, new_key)
                _write_env(env_path, updated)
                print(f"Updated {env_path} with new {ENV_KEY}. Restart pin.service to apply.")
            return 0

        # Decrypt all with old key first (fail fast)
        plaintext: dict[tuple[str, str], str] = {}
        for r in rows:
            try:
                pt = old_f.decrypt(r.api_key_enc.encode("utf-8")).decode("utf-8")
            except Exception as e:
                print(
                    f"ERROR: failed to decrypt key for org={r.org_id} provider={r.provider}. "
                    f"Old {ENV_KEY} is likely wrong. Details: {e}",
                    file=sys.stderr,
                )
                return 3
            plaintext[(r.org_id, r.provider)] = pt

        # Re-encrypt
        updates: list[tuple[ProviderRow, str]] = []
        for r in rows:
            pt = plaintext[(r.org_id, r.provider)]
            token = new_f.encrypt(pt.encode("utf-8")).decode("utf-8")
            updates.append((r, token))

        print(f"Will rotate {len(updates)} provider key(s).")

        if args.dry_run:
            print("DRY RUN: no changes written.")
            return 0

        # Backup env file
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup_path = env_path.with_suffix(env_path.suffix + f".bak.{stamp}")
        shutil.copy2(env_path, backup_path)

        # Update env file
        updated_env = _upsert_env_value(env_text, ENV_KEY, new_key)
        _write_env(env_path, updated_env)

        # Update DB in a transaction
        with conn:
            for row, token in updates:
                _update_provider_row(conn, row, token)

        print(f"Env updated: {env_path} (backup: {backup_path})")
        print("DB updated: provider keys re-encrypted.")
        print("Next: sudo systemctl restart pin.service")
        return 0
    finally:
        conn.close()


def _write_env(path: Path, text: str) -> None:
    # Keep strict perms for secrets
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


if __name__ == "__main__":
    raise SystemExit(main())
