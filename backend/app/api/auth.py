# -*- coding: utf-8 -*-
"""Authentication endpoints (T-004): register, login, current user.

Only HTTP wiring lives here. Hashing and token primitives are in
``app.core.security``; reusable dependencies are in ``app.api.deps``.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import Role, User, UserRole
from app.schemas.auth import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Default role assigned to every self-registered user.
DEFAULT_ROLE_CODE = "client"
DEFAULT_ROLE_TITLE = "Client"


def _get_or_create_role(db: Session, code: str, title: str) -> Role:
    """Return the role with ``code``, creating it when the dictionary is empty.

    The Role table is a reference dictionary. Seeding it is normally done by a
    separate script, but registration must stay functional on a fresh database,
    so the role is resolved lazily instead of assuming a pre-seeded row.
    """
    role = db.execute(select(Role).where(Role.code == code)).scalar_one_or_none()
    if role is None:
        role = Role(code=code, title=title)
        db.add(role)
        db.flush()
    return role


def _build_user_response(user: User) -> UserResponse:
    """Map a User ORM object (with loaded roles) to the public schema."""
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=sorted({link.role.code for link in user.user_roles if link.role is not None}),
    )


def _issue_token(user: User) -> Token:
    """Create a JWT whose subject is the user id."""
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=Token, status_code=status.HTTP_200_OK)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> Token:
    """Create a new user with the default 'client' role and return a JWT."""
    email = payload.email.lower()
    existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    user = User(
        email=email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.flush()

    role = _get_or_create_role(db, DEFAULT_ROLE_CODE, DEFAULT_ROLE_TITLE)
    db.add(UserRole(user_id=user.id, role_id=role.id))

    db.commit()
    db.refresh(user)

    return _issue_token(user)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Verify credentials and return a JWT.

    The same error is returned for an unknown email and a wrong password so the
    endpoint does not leak which accounts exist.
    """
    email = payload.email.lower()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return _issue_token(user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the authenticated user's profile with their role codes."""
    return _build_user_response(current_user)
