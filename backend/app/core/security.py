# -*- coding: utf-8 -*-
"""Password hashing and JWT helpers (T-004).

Security notes:
- Passwords are never stored in plain text; only bcrypt hashes.
- JWT payloads carry a subject (``sub``) with the user id and an expiry (``exp``).
- All secrets come from settings; nothing is hardcoded here.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt is the single supported scheme. ``deprecated="auto"`` keeps the door open
# for future migrations without breaking verification of existing hashes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Return a bcrypt hash for the given plain-text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Return True when the plain password matches the stored hash."""
    try:
        return pwd_context.verify(plain_password, password_hash)
    except ValueError:
        # Malformed / unknown hash: treat as a failed verification, never crash.
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode a signed JWT with an expiry taken from settings by default.

    Args:
        data: Claims to embed. A ``sub`` claim is expected to hold the user id.
        expires_delta: Optional override for the token lifetime.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT. Returns the payload or None when invalid."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
