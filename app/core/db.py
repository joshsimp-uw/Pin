from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import settings


def connect() -> sqlite3.Connection:
    """Open a SQLite connection with safe defaults.

    Notes
    -----
    - WAL mode improves concurrency for read/write workloads typical of chat apps.
    - Foreign keys must be enabled per connection in SQLite.
    """
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_schema(schema_path: str = "data/schema.sql") -> None:
    """Create/upgrade the DB schema for a freshly deployed org site."""
    sql_path = Path(schema_path)
    if not sql_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    sql = sql_path.read_text(encoding="utf-8")
    conn = connect()
    try:
        # Schema includes sqlite-vec virtual tables. Load the extension for this
        # connection if available.
        try:
            conn.enable_load_extension(True)
            import sqlite_vec  # type: ignore

            sqlite_vec.load(conn)
        except Exception as e:
            raise RuntimeError(
                "Failed to load sqlite-vec extension required by the schema. "
                "Install 'sqlite-vec' and ensure your sqlite3 build supports extension loading."
            ) from e
        finally:
            try:
                conn.enable_load_extension(False)
            except Exception:
                pass

        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
