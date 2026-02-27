from __future__ import annotations

import json
import uuid
from typing import Any

from app.core.db import connect


def ensure_org(org_id: str, name: str | None = None) -> None:
    """Ensure an org row exists (idempotent)."""
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


def set_session_title(session_id: str, title: str) -> None:
    conn = connect()
    try:
        conn.execute("UPDATE sessions SET title=?, updated_at=datetime('now') WHERE session_id=?", (title, session_id))
        conn.commit()
    finally:
        conn.close()


def close_session(session_id: str) -> None:
    conn = connect()
    try:
        conn.execute(
            "UPDATE sessions SET status='closed', closed_at=datetime('now'), updated_at=datetime('now') WHERE session_id=?",
            (session_id,),
        )
        conn.commit()
    finally:
        conn.close()


def link_session_to_ticket(session_id: str, ticket_id: str) -> None:
    conn = connect()
    try:
        conn.execute(
            "UPDATE sessions SET ticket_id=?, updated_at=datetime('now') WHERE session_id=?",
            (ticket_id, session_id),
        )
        conn.commit()
    finally:
        conn.close()


def list_open_sessions(org_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """Admin/global: list open sessions for an org."""
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, user_id, title, ticket_id, turns, category, status, created_at, updated_at, closed_at
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


def list_user_sessions(org_id: str, user_id: str, status: str, limit: int = 100) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, title, ticket_id, turns, category, status, created_at, updated_at, closed_at
            FROM sessions
            WHERE org_id=? AND user_id=? AND status=?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (org_id, user_id, status, int(limit)),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_session(org_id: str, user_id: str, session_id: str) -> dict[str, Any] | None:
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT session_id, org_id, user_id, title, ticket_id, turns, category, status, created_at, updated_at, closed_at
            FROM sessions
            WHERE session_id=?
            """,
            (session_id,),
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        if d["org_id"] != org_id or d["user_id"] != user_id:
            return None
        return d
    finally:
        conn.close()


def list_session_messages(org_id: str, user_id: str, session_id: str, limit: int = 500) -> list[dict[str, Any]]:
    conn = connect()
    try:
        # Ensure ownership
        ok = conn.execute(
            "SELECT 1 FROM sessions WHERE session_id=? AND org_id=? AND user_id=? LIMIT 1",
            (session_id, org_id, user_id),
        ).fetchone()
        if not ok:
            return []
        cur = conn.execute(
            """
            SELECT message_id, role, content, citations_json, created_at
            FROM messages
            WHERE session_id=?
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (session_id, int(limit)),
        )
        out: list[dict[str, Any]] = []
        for r in cur.fetchall():
            d = dict(r)
            try:
                d["citations"] = json.loads(d.pop("citations_json") or "[]")
            except Exception:
                d["citations"] = []
                d.pop("citations_json", None)
            out.append(d)
        return out
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


def list_user_tickets(org_id: str, user_id: str, status: str, limit: int = 100) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT ticket_id, session_id, summary, category, impact, urgency, status, created_at, closed_at
            FROM tickets
            WHERE org_id=? AND user_id=? AND status=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (org_id, user_id, status, int(limit)),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_ticket(org_id: str, user_id: str, ticket_id: str) -> dict[str, Any] | None:
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT ticket_id, org_id, user_id, session_id, summary, category, impact, urgency, status,
                   escalation_reason, rendered_text, diagnostics_json, steps_attempted_json, citations_json,
                   created_at, closed_at
            FROM tickets
            WHERE ticket_id=?
            """,
            (ticket_id,),
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        if d["org_id"] != org_id or d["user_id"] != user_id:
            return None
        for k in ["diagnostics_json", "steps_attempted_json", "citations_json"]:
            try:
                d[k.replace("_json", "")] = json.loads(d.pop(k) or ("{}" if k == "diagnostics_json" else "[]"))
            except Exception:
                d[k.replace("_json", "")] = {} if k == "diagnostics_json" else []
                d.pop(k, None)
        return d
    finally:
        conn.close()


def list_ticket_sessions(org_id: str, user_id: str, ticket_id: str) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT session_id, title, status, created_at, updated_at, closed_at
            FROM sessions
            WHERE org_id=? AND user_id=? AND ticket_id=?
            ORDER BY created_at ASC
            """,
            (org_id, user_id, ticket_id),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def list_users(org_id: str, limit: int = 200) -> list[dict[str, Any]]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT user_id, first_name, last_name, email, role, created_at
            FROM users
            WHERE org_id=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (org_id, int(limit)),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()
