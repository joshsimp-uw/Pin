from __future__ import annotations

from fastapi import APIRouter, Body, Header, HTTPException

from app.api.deps import bearer_token
from app.core.auth import get_user_by_email, issue_token, require_user, verify_user_password, set_user_password

router = APIRouter(tags=["auth"])


@router.post("/auth/login")
def auth_login(payload: dict = Body(...)) -> dict:
    org_id = str(payload.get("org_id") or "ACME").strip() or "ACME"
    email = str(payload.get("email") or "").strip()
    password = str(payload.get("password") or "").strip()
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password are required")

    u = get_user_by_email(org_id=org_id, email=email)
    if not u:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_user_password(user_id=u.user_id, password=password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = issue_token(org_id=org_id, user_id=u.user_id)
    return {
        "token": token,
        "user": {
            "user_id": u.user_id,
            "org_id": u.org_id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": u.role,
        },
    }


@router.get("/auth/me")
def auth_me(authorization: str | None = Header(default=None)) -> dict:
    u = require_user(bearer_token(authorization))
    return {
        "user": {
            "user_id": u.user_id,
            "org_id": u.org_id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": u.role,
        }
    }


@router.post("/auth/change_password")
def auth_change_password(authorization: str | None = Header(default=None), payload: dict = Body(...)) -> dict:
    """Allow an authenticated user to change their password."""
    u = require_user(bearer_token(authorization))
    current_password = str(payload.get("current_password") or "").strip()
    new_password = str(payload.get("new_password") or "").strip()
    if not current_password or not new_password:
        raise HTTPException(status_code=400, detail="current_password and new_password are required")
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="new_password must be at least 8 characters")
    if not verify_user_password(user_id=u.user_id, password=current_password):
        raise HTTPException(status_code=401, detail="Invalid current password")

    set_user_password(user_id=u.user_id, password=new_password)
    return {"status": "ok"}
