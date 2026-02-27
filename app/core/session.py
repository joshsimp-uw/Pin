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
    title: str | None = None
    ticket_id: str | None = None
    closed_at: str | None = None


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
        title=None,
        ticket_id=None,
        closed_at=None,
    )
    save_session(state)
    return state


def load_session(session_id: str) -> SessionState:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, org_id, user_id, title, ticket_id, turns, category, status,
                   collected_json, steps_attempted_json, closed_at
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
            title=row["title"],
            ticket_id=row["ticket_id"],
            turns=int(row["turns"]),
            category=row["category"],
            status=row["status"],
            collected=json.loads(row["collected_json"]),
            steps_attempted=json.loads(row["steps_attempted_json"]),
            closed_at=row["closed_at"],
        )
    finally:
        conn.close()


def save_session(state: SessionState) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO sessions(
              session_id, org_id, user_id, title, ticket_id, turns, category, status,
              collected_json, steps_attempted_json, updated_at, closed_at
            )
            VALUES(?,?,?,?,?,?,?,?,?,?, datetime('now'), ?)
            ON CONFLICT(session_id) DO UPDATE SET
              org_id=excluded.org_id,
              user_id=excluded.user_id,
              title=excluded.title,
              ticket_id=excluded.ticket_id,
              turns=excluded.turns,
              category=excluded.category,
              status=excluded.status,
              collected_json=excluded.collected_json,
              steps_attempted_json=excluded.steps_attempted_json,
              updated_at=datetime('now'),
              closed_at=excluded.closed_at
            """,
            (
                state.session_id,
                state.org_id,
                state.user_id,
                state.title,
                state.ticket_id,
                int(state.turns),
                state.category,
                state.status,
                json.dumps(state.collected),
                json.dumps(state.steps_attempted),
                state.closed_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()
