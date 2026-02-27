from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    # org_id/user_id are deprecated: the API derives these from the Bearer token.
    # They remain for backward compatibility with older clients.
    org_id: str | None = None
    user_id: str | None = None
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


class Action(BaseModel):
    action_id: str
    label: str


class ActionResponse(BaseModel):
    type: Literal["action"] = "action"
    message: str
    actions: list[Action] = Field(default_factory=list)
    # If provided, the UI can render additional details.
    meta: dict[str, Any] = Field(default_factory=dict)


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
    rendered: str


ChatResponse = AnswerResponse | ActionResponse | TicketResponse
