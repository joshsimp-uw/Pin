from __future__ import annotations

from fastapi import APIRouter, Body, Header, HTTPException

from app.api.deps import bearer_token
from app.core.auth import get_user_by_email, issue_token, require_user, verify_user_password

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
