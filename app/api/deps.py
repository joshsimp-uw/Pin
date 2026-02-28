from __future__ import annotations

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import require_admin, require_user
from app.core.config import settings


def bearer_token(authorization: str | None) -> str | None:
    """Extract a Bearer token from the Authorization header."""
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip() or None
    return None


def require_user_from_auth_header(authorization: str | None):
    return require_user(bearer_token(authorization))


def require_admin_from_auth_header(authorization: str | None):
    return require_admin(bearer_token(authorization))


def require_admin_token(x_admin_token: str | None) -> None:
    """Break-glass token check used for bootstrap in non-dev."""
    if not settings.admin_token:
        raise HTTPException(status_code=500, detail="Admin token is not configured on the server")
    if not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Security scheme used by Swagger's "Authorize" button.
# Add this as a dependency at the route/router/app level to display the lock icon in /docs.
bearer_scheme = HTTPBearer(auto_error=False)


def get_token_swagger(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str | None:
    """
    Bridge for Swagger: extracts just the token string from HTTPBearer credentials.
    Returns None when no credentials are provided so routes can still choose to
    fallback to header-based parsing if desired.
    """
    if not creds:
        return None
    return creds.credentials


def require_user_swagger(token: str | None = Depends(get_token_swagger)):
    """
    Swagger-friendly user dependency.
    Reuses the same core validation (require_user) as the header-based path.
    """
    return require_user(token)
