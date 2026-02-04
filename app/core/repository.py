from __future__ import annotations

import json
import uuid
from typing import Any, Iterable

from app.core.db import connect


def ensure_org(org_id: str, name: str | None = None) -> None:
    """Ensure an org row exists.

    In a per-org DB deployment, this should be called once at install time,
    but it's harmless to call on demand (idempotent).
    """
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO orgs(org_id, name)
            VALUES(?, COALESCE(?, ?))
            ON CONFLICT(org_id) DO UPDATE SET
              name=COALESCE(excluded.name, orgs.name)
            """,
            (org_id, name, org_id),
        )
        conn.commit()
    finally:
        conn.close()


def ensure_department(dept_id: int, dept_name: str) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO departments(dept_id, dept_name)
            VALUES(?, ?)
            ON CONFLICT(dept_id) DO UPDATE SET
              dept_name=excluded.dept_name
            """,
            (int(dept_id), dept_name),
        )
        conn.commit()
    finally:
        conn.close()


def ensure_user(
    *,
    org_id: str,
    user_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    role: str = "end_user",
    dept_id: int | None = None,
) -> None:
    """Ensure a user row exists."""
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO users(user_id, org_id, first_name, last_name, email, role, dept_id)
            VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
              org_id=excluded.org_id,
              first_name=COALESCE(excluded.first_name, users.first_name),
              last_name=COALESCE(excluded.last_name, users.last_name),
              email=COALESCE(excluded.email, users.email),
              role=COALESCE(excluded.role, users.role),
              dept_id=COALESCE(excluded.dept_id, users.dept_id)
            """,
            (user_id, org_id, first_name, last_name, email, role, dept_id),
        )
        conn.commit()
    finally:
        conn.close()


def insert_message(
    *,
    session_id: str,
    role: str,
    content: str,
    citations: list[dict[str, Any]] | None = None,
) -> str:
    message_id = str(uuid.uuid4())
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO messages(message_id, session_id, role, content, citations_json)
            VALUES(?,?,?,?,?)
            """,
            (message_id, session_id, role, content, json.dumps(citations or [])),
        )
        conn.commit()
        return message_id
    finally:
        conn.close()


def insert_ticket(
    *,
    org_id: str,
    user_id: str,
    session_id: str | None,
    summary: str,
    category: str,
    impact: str,
    urgency: str,
    escalation_reason: str,
    rendered_text: str,
    diagnostics: dict[str, Any] | None = None,
    steps_attempted: list[str] | None = None,
    citations: list[dict[str, Any]] | None = None,
) -> str:
    ticket_id = str(uuid.uuid4())
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO tickets(
              ticket_id, org_id, user_id, session_id, summary, category, impact, urgency,
              status, escalation_reason, rendered_text,
              diagnostics_json, steps_attempted_json, citations_json
            )
            VALUES(?,?,?,?,?,?,?,?, 'created', ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                org_id,
                user_id,
                session_id,
                summary,
                category,
                impact,
                urgency,
                escalation_reason,
                rendered_text,
                json.dumps(diagnostics or {}),
                json.dumps(steps_attempted or []),
                json.dumps(citations or []),
            ),
        )
        conn.commit()
        return ticket_id
    finally:
        conn.close()


def list_open_sessions(org_id: str, limit: int = 50) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, user_id, turns, category, status, created_at, updated_at
            FROM sessions
            WHERE org_id=? AND status='open'
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (org_id, int(limit)),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def list_tickets(org_id: str, status: str, limit: int = 50) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT ticket_id, user_id, session_id, summary, category, impact, urgency, status, created_at, closed_at
            FROM tickets
            WHERE org_id=? AND status=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (org_id, status, int(limit)),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()
