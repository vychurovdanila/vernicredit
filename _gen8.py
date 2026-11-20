# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\models\ai.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0414\u0430\u043d\u043d\u044b\u0435 \u0434\u043b\u044f AI: \u043b\u043e\u0433\u0438 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439 \u0438 \u0438\u0441\u0445\u043e\u0434\u044b \u0434\u0435\u043b.\"\"\"

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ActionLog(Base):
    \"\"\"\u041b\u043e\u0433 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 \u0438 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u043e\u0432.\"\"\"

    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_role: Mapped[str | None] = mapped_column(String(32), nullable=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_id: Mapped[int | None] = mapped_column(
        ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application | None"] = relationship(backref="action_logs")


class CaseOutcome(Base):
    \"\"\"\u0418\u0442\u043e\u0433 \u0434\u0435\u043b\u0430: \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442, \u0441\u0440\u043e\u043a, \u0441\u0443\u043c\u043c\u0430, \u043f\u0440\u043e\u0446\u0435\u043d\u0442.\"\"\"

    __tablename__ = "case_outcomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    result: Mapped[str] = mapped_column(String(32), nullable=False)
    days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sum: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(backref="case_outcomes")
"""

FILES[r"app\models\integration.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u041f\u0440\u0438\u0432\u044f\u0437\u043a\u0430 Telegram-\u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430 \u043a \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044e.\"\"\"

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TelegramLink(Base):
    \"\"\"\u0421\u0432\u044f\u0437\u044c users \u2194 Telegram chat.\"\"\"

    __tablename__ = "telegram_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(backref="telegram_links")
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
