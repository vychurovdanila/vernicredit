# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\models\document.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0417\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043d\u044b\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b.\"\"\"

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Document(Base):
    \"\"\"\u0424\u0430\u0439\u043b, \u043f\u0440\u0438\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0439 \u043a \u0437\u0430\u044f\u0432\u043a\u0435.\"\"\"

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    doc_type: Mapped[str] = mapped_column(String(64), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="uploaded", server_default="uploaded"
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(backref="documents")
"""

FILES[r"app\models\finance.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0412\u043e\u0437\u0432\u0440\u0430\u0442\u044b \u0438 \u043f\u043b\u0430\u0442\u0435\u0436\u0438.\"\"\"

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Return(Base):
    \"\"\"\u0424\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u0434\u0435\u043d\u0435\u0433 \u043e\u0442 \u0431\u0430\u043d\u043a\u0430.\"\"\"

    __tablename__ = "returns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    proof_file: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", server_default="pending"
    )
    verified_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(backref="returns")
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="return_record", cascade="all, delete-orphan"
    )


class Payment(Base):
    \"\"\"\u041a\u043e\u043c\u0438\u0441\u0441\u0438\u044f \u0441\u0435\u0440\u0432\u0438\u0441\u0430, \u0443\u043f\u043b\u0430\u0447\u0435\u043d\u043d\u0430\u044f \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u043c.\"\"\"

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    return_id: Mapped[int | None] = mapped_column(
        ForeignKey("returns.id", ondelete="SET NULL"), nullable=True, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", server_default="pending"
    )
    receipt_file: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    verified_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    application: Mapped["Application"] = relationship(backref="payments")
    return_record: Mapped["Return | None"] = relationship(back_populates="payments")
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
