# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u00ab\u0412\u0435\u0440\u043d\u0438 \u041a\u0440\u0435\u0434\u0438\u0442\u00bb.\"\"\"
"""

FILES[r"app\db\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0421\u043b\u043e\u0439 \u0434\u043e\u0441\u0442\u0443\u043f\u0430 \u043a \u0431\u0430\u0437\u0435 \u0434\u0430\u043d\u043d\u044b\u0445.\"\"\"
"""

FILES[r"app\db\base.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0414\u0435\u043a\u043b\u0430\u0440\u0430\u0442\u0438\u0432\u043d\u0430\u044f \u0431\u0430\u0437\u0430 \u0434\u043b\u044f \u0432\u0441\u0435\u0445 \u043c\u043e\u0434\u0435\u043b\u0435\u0439.\"\"\"

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    \"\"\"\u041e\u0431\u0449\u0438\u0439 \u043a\u043b\u0430\u0441\u0441-\u043e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f ORM-\u043c\u043e\u0434\u0435\u043b\u0435\u0439.\"\"\"

    pass
"""

FILES[r"app\db\session.py"] = """# -*- coding: utf-8 -*-
\"\"\"Engine \u0438 SessionLocal. \u0410\u0434\u0440\u0435\u0441 \u0411\u0414 \u0431\u0435\u0440\u0451\u0442\u0441\u044f \u0438\u0437 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f DATABASE_URL.\"\"\"

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vernicredit.db")

# \u0414\u043b\u044f SQLite \u043d\u0443\u0436\u0435\u043d check_same_thread=False, \u0434\u043b\u044f \u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0445 \u0411\u0414 \u044d\u0442\u043e\u0442 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 \u043d\u0435 \u043f\u0435\u0440\u0435\u0434\u0430\u0451\u043c.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
"""

FILES[r"app\models\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0420\u0435\u0435\u0441\u0442\u0440 \u0432\u0441\u0435\u0445 ORM-\u043c\u043e\u0434\u0435\u043b\u0435\u0439.\n\n\u0418\u043c\u043f\u043e\u0440\u0442 \u043c\u043e\u0434\u0435\u043b\u0435\u0439 \u0437\u0434\u0435\u0441\u044c \u043d\u0443\u0436\u0435\u043d, \u0447\u0442\u043e\u0431\u044b \u043e\u043d\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043b\u0438\u0441\u044c \u0432 Base.metadata\n(\u0434\u043b\u044f Alembic autogenerate \u0438 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0442\u0430\u0431\u043b\u0438\u0446).\n\"\"\"

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
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
