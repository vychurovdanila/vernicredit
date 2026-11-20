# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\models\application.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0417\u0430\u044f\u0432\u043a\u0438 \u0438 \u0438\u0441\u0442\u043e\u0440\u0438\u044f \u0441\u0442\u0430\u0442\u0443\u0441\u043e\u0432.\"\"\"

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Application(Base):
    \"\"\"\u0417\u0430\u044f\u0432\u043a\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0430 \u043d\u0430 \u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u0441\u0442\u0440\u0430\u0445\u043e\u0432\u043a\u0438/\u043f\u0435\u0440\u0435\u043f\u043b\u0430\u0442\u044b.\"\"\"

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    credit_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    bank: Mapped[str | None] = mapped_column(String(255), nullable=True)
    loan_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="new", server_default="new", index=True
    )
    pre_return_min: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    pre_return_max: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    final_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    total_returned: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    total_commission: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    expected_payout_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    utm_source: Mapped[str | None] = mapped_column(String(128), nullable=True)
    draft_token: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    suspended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship(backref="applications")
    status_history: Mapped[list["StatusHistory"]] = relationship(
        back_populates="application", cascade="all, delete-orphan"
    )


class StatusHistory(Base):
    \"\"\"\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0441\u043c\u0435\u043d\u044b \u0441\u0442\u0430\u0442\u0443\u0441\u043e\u0432 \u0437\u0430\u044f\u0432\u043a\u0438.\"\"\"

    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(back_populates="status_history")
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
