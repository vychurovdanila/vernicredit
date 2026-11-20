# -*- coding: utf-8 -*-
"""Engine и SessionLocal. Адрес БД берётся из переменной окружения DATABASE_URL."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vernicredit.db")

# Для SQLite нужен check_same_thread=False, для остальных БД этот параметр не передаём.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
