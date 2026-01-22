from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    org_id: str = "demo-org"
    user_id: str = "demo-user"
    # Optional: user/device context from login/LDAP/etc.
    context: dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    source_id: str
    title: str
    snippet: str


class AnswerResponse(BaseModel):
    type: Literal["answer"] = "answer"
    message: str
    citations: list[Citation] = Field(default_factory=list)
    next_question: str | None = None
    collected: dict[str, Any] = Field(default_factory=dict)


class Ticket(BaseModel):
    summary: str
    category: str
    impact: Literal["low", "medium", "high"] = "medium"
    urgency: Literal["low", "medium", "high"] = "medium"
    user: dict[str, Any] = Field(default_factory=dict)
    device: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    steps_attempted: list[str] = Field(default_factory=list)
    error_text: str | None = None
    escalation_reason: str
    citations: list[Citation] = Field(default_factory=list)


class TicketResponse(BaseModel):
    type: Literal["ticket"] = "ticket"
    ticket: Ticket
    # This is what you can email or save as a text file.
    rendered: str


ChatResponse = AnswerResponse | TicketResponse
