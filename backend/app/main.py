# -*- coding: utf-8 -*-
"""FastAPI application entry point (T-003 skeleton).

Run locally:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health as health_router
from app.core.config import settings

app = FastAPI(title="Vernicredit API", version="0.1.0")

# CORS: Bearer tokens travel in headers, so credentials must stay disabled.
# Origins come from settings and never include a wildcard.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(health_router.router)
