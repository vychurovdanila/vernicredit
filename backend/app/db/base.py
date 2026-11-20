# -*- coding: utf-8 -*-
"""Декларативная база для всех моделей."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Общий класс-основание для ORM-моделей."""

    pass
