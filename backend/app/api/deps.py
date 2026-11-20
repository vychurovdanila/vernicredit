# -*- coding: utf-8 -*-
"""Reusable FastAPI dependencies (T-004).

Business logic stays out of here: this module only resolves HTTP concerns
(bearer token extraction, DB session, current user lookup).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User

# auto_error=False lets us raise a consistent 401 (with WWW-Authenticate)
# instead of the default 403 produced by HTTPBearer when the header is missing.
bearer_scheme = HTTPBearer(auto_error=False)

# 401 with WWW-Authenticate for every auth failure (missing/invalid/expired token).
_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db() -> Session:
    """Yield a database session and always close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from the ``Authorization: Bearer`` header.

    Raises:
        HTTPException: 401 when the token is missing, invalid, expired,
            references an unknown user, or the user is deactivated.
    """
    if credentials is None or not credentials.credentials:
        raise _CREDENTIALS_EXCEPTION

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise _CREDENTIALS_EXCEPTION

    subject = payload.get("sub")
    if subject is None:
        raise _CREDENTIALS_EXCEPTION

    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise _CREDENTIALS_EXCEPTION from None

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise _CREDENTIALS_EXCEPTION

    return user
