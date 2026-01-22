from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.core.config import settings


@dataclass
class SessionState:
    session_id: str
    turns: int
    category: str | None
    collected: dict[str, Any]
    steps_attempted: list[str]


def _conn() -> sqlite3.Connection:
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            turns INTEGER NOT NULL,
            category TEXT,
            collected_json TEXT NOT NULL,
            steps_attempted_json TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def new_session() -> SessionState:
    sid = str(uuid.uuid4())
    state = SessionState(session_id=sid, turns=0, category=None, collected={}, steps_attempted=[])
    save_session(state)
    return state


def load_session(session_id: str) -> SessionState:
    conn = _conn()
    cur = conn.execute(
        "SELECT session_id, turns, category, collected_json, steps_attempted_json FROM sessions WHERE session_id=?",
        (session_id,),
    )
    row = cur.fetchone()
    if not row:
        # Unknown session -> create a new one using the requested id
        state = SessionState(session_id=session_id, turns=0, category=None, collected={}, steps_attempted=[])
        save_session(state)
        return state

    return SessionState(
        session_id=row[0],
        turns=int(row[1]),
        category=row[2],
        collected=json.loads(row[3]),
        steps_attempted=json.loads(row[4]),
    )


def save_session(state: SessionState) -> None:
    conn = _conn()
    conn.execute(
        """
        INSERT INTO sessions(session_id, turns, category, collected_json, steps_attempted_json)
        VALUES(?,?,?,?,?)
        ON CONFLICT(session_id) DO UPDATE SET
          turns=excluded.turns,
          category=excluded.category,
          collected_json=excluded.collected_json,
          steps_attempted_json=excluded.steps_attempted_json
        """,
        (
            state.session_id,
            int(state.turns),
            state.category,
            json.dumps(state.collected),
            json.dumps(state.steps_attempted),
        ),
    )
    conn.commit()
