# -*- coding: utf-8 -*-
"""Реестр всех ORM-моделей.

Импорт моделей здесь нужен, чтобы они регистрировались в Base.metadata
(для Alembic autogenerate и создания таблиц).
"""

from app.models.ai import ActionLog, CaseOutcome
from app.models.application import Application, StatusHistory
from app.models.communication import Message, Notification
from app.models.content import BankTemplate, FaqEntry
from app.models.document import Document
from app.models.finance import Payment, Return
from app.models.integration import TelegramLink
from app.models.user import Role, User, UserRole

__all__ = [
    "ActionLog",
    "Application",
    "BankTemplate",
    "CaseOutcome",
    "Document",
    "FaqEntry",
    "Message",
    "Notification",
    "Payment",
    "Return",
    "Role",
    "StatusHistory",
    "TelegramLink",
    "User",
    "UserRole",
]
