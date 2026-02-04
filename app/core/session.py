from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from typing import Any

from app.core.db import connect


@dataclass
class SessionState:
    session_id: str
    org_id: str
    user_id: str
    turns: int
    category: str | None
    status: str
    collected: dict[str, Any]
    steps_attempted: list[str]


def new_session(*, org_id: str, user_id: str) -> SessionState:
    sid = str(uuid.uuid4())
    state = SessionState(
        session_id=sid,
        org_id=org_id,
        user_id=user_id,
        turns=0,
        category=None,
        status="open",
        collected={},
        steps_attempted=[],
    )
    save_session(state)
    return state


def load_session(session_id: str) -> SessionState:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, org_id, user_id, turns, category, status, collected_json, steps_attempted_json
            FROM sessions
            WHERE session_id=?
            """,
            (session_id,),
        )
        row = cur.fetchone()
        if not row:
            raise KeyError(session_id)

        return SessionState(
            session_id=row["session_id"],
            org_id=row["org_id"],
            user_id=row["user_id"],
            turns=int(row["turns"]),
            category=row["category"],
            status=row["status"],
            collected=json.loads(row["collected_json"]),
            steps_attempted=json.loads(row["steps_attempted_json"]),
        )
    finally:
        conn.close()


def save_session(state: SessionState) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO sessions(
              session_id, org_id, user_id, turns, category, status, collected_json, steps_attempted_json, updated_at
            )
            VALUES(?,?,?,?,?,?,?,?, datetime('now'))
            ON CONFLICT(session_id) DO UPDATE SET
              org_id=excluded.org_id,
              user_id=excluded.user_id,
              turns=excluded.turns,
              category=excluded.category,
              status=excluded.status,
              collected_json=excluded.collected_json,
              steps_attempted_json=excluded.steps_attempted_json,
              updated_at=datetime('now')
            """,
            (
                state.session_id,
                state.org_id,
                state.user_id,
                int(state.turns),
                state.category,
                state.status,
                json.dumps(state.collected),
                json.dumps(state.steps_attempted),
            ),
        )
        conn.commit()
    finally:
        conn.close()