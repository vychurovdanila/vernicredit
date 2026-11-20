# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\models\communication.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u0438 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f.\"\"\"

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Message(Base):
    \"\"\"\u0415\u0434\u0438\u043d\u044b\u0439 \u0434\u0438\u0430\u043b\u043e\u0433 \u043f\u043e \u0437\u0430\u044f\u0432\u043a\u0435 (\u041b\u041a \u0438 Telegram \u2014 \u0434\u0432\u0430 \u0444\u0440\u043e\u043d\u0442\u0430 \u043e\u0434\u043d\u043e\u0433\u043e \u0447\u0430\u0442\u0430).\"\"\"

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sender_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    channel: Mapped[str] = mapped_column(
        String(16), nullable=False, default="lk", server_default="lk"
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(backref="messages")


class Notification(Base):
    \"\"\"\u041b\u043e\u0433 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u044b\u0445 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439.\"\"\"

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    application_id: Mapped[int | None] = mapped_column(
        ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True
    )
    channel: Mapped[str] = mapped_column(
        String(16), nullable=False, default="lk", server_default="lk"
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", server_default="pending"
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(backref="notifications")
"""

FILES[r"app\models\content.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u041a\u043e\u043d\u0442\u0435\u043d\u0442: \u0448\u0430\u0431\u043b\u043e\u043d\u044b \u043f\u0438\u0441\u0435\u043c \u0438 FAQ.\"\"\"

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BankTemplate(Base):
    \"\"\"\u0428\u0430\u0431\u043b\u043e\u043d \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u0434\u043b\u044f \u0431\u0430\u043d\u043a\u0430.\"\"\"

    __tablename__ = "bank_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    template_type: Mapped[str] = mapped_column(String(64), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class FaqEntry(Base):
    \"\"\"\u0412\u043e\u043f\u0440\u043e\u0441-\u043e\u0442\u0432\u0435\u0442 \u0434\u043b\u044f \u0431\u043e\u0442\u0430 \u0438 \u043b\u0435\u043d\u0434\u0438\u043d\u0433\u0430.\"\"\"

    __tablename__ = "faq_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(512), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
