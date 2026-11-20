# -*- coding: utf-8 -*-
"""Health check endpoint used for uptime probing and smoke tests."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])

API_VERSION = "0.1.0"


@router.get("/api/health")
def health() -> dict[str, str]:
    """Return a static liveness payload."""
    return {"status": "ok", "version": API_VERSION}
