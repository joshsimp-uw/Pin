#!/usr/bin/env python3
"""Migrate an existing Pin SQLite DB to the current schema.

Usage:
  ./scripts/migrate_db.py --sqlite-path data/pin.db

This script is intentionally dependency-free (std-lib only).
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (table,)
    ).fetchone()
    return bool(row)


def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def migrate(conn: sqlite3.Connection) -> None:
    # sessions: title, ticket_id, closed_at
    if _table_exists(conn, "sessions"):
        if not _has_column(conn, "sessions", "title"):
            conn.execute("ALTER TABLE sessions ADD COLUMN title TEXT")
        if not _has_column(conn, "sessions", "ticket_id"):
            conn.execute("ALTER TABLE sessions ADD COLUMN ticket_id TEXT")
        if not _has_column(conn, "sessions", "closed_at"):
            conn.execute("ALTER TABLE sessions ADD COLUMN closed_at TEXT")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_ticket ON sessions(ticket_id)")

    # users: soft-disable flags
    if _table_exists(conn, "users"):
        if not _has_column(conn, "users", "is_disabled"):
            conn.execute("ALTER TABLE users ADD COLUMN is_disabled INTEGER NOT NULL DEFAULT 0")
        if not _has_column(conn, "users", "disabled_at"):
            conn.execute("ALTER TABLE users ADD COLUMN disabled_at TEXT")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_disabled ON users(org_id, is_disabled)")

    conn.commit()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sqlite-path", default="data/pin.db")
    args = ap.parse_args()

    db_path = Path(args.sqlite_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        migrate(conn)
    finally:
        conn.close()

    print("OK: migrations applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
