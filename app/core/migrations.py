from __future__ import annotations

import sqlite3


def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)  # r[1] is name


def run_migrations(conn: sqlite3.Connection) -> None:
    """Idempotent schema migrations for existing databases.

    The app ships a schema.sql for fresh installs. Older DBs need ALTERs.
    Keep this lightweight and dependency-free.
    """

    # sessions: title, ticket_id, closed_at
    if _table_exists(conn, "sessions"):
        if not _has_column(conn, "sessions", "title"):
            conn.execute("ALTER TABLE sessions ADD COLUMN title TEXT")
        if not _has_column(conn, "sessions", "ticket_id"):
            conn.execute("ALTER TABLE sessions ADD COLUMN ticket_id TEXT")
        if not _has_column(conn, "sessions", "closed_at"):
            conn.execute("ALTER TABLE sessions ADD COLUMN closed_at TEXT")

        # Indexes are safe to create repeatedly with IF NOT EXISTS
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_ticket ON sessions(ticket_id)")

    # users: soft-disable flags (historical retention)
    if _table_exists(conn, "users"):
        if not _has_column(conn, "users", "is_disabled"):
            conn.execute("ALTER TABLE users ADD COLUMN is_disabled INTEGER NOT NULL DEFAULT 0")
        if not _has_column(conn, "users", "disabled_at"):
            conn.execute("ALTER TABLE users ADD COLUMN disabled_at TEXT")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_disabled ON users(org_id, is_disabled)")

    conn.commit()


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (table,)
    ).fetchone()
    return bool(row)
