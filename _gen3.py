# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u041f\u0430\u043a\u0435\u0442 backend-\u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f.\"\"\"
"""

FILES[r"app\models\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0432\u0441\u0435\u0445 ORM-\u043c\u043e\u0434\u0435\u043b\u0435\u0439.

\u0418\u043c\u043f\u043e\u0440\u0442 \u043c\u043e\u0434\u0435\u043b\u0435\u0439 \u0437\u0434\u0435\u0441\u044c \u043d\u0443\u0436\u0435\u043d, \u0447\u0442\u043e\u0431\u044b Alembic \u0432\u0438\u0434\u0435\u043b \u043c\u0435\u0442\u0430\u0434\u0430\u043d\u043d\u044b\u0435 \u0432\u0441\u0435\u0445 \u0442\u0430\u0431\u043b\u0438\u0446.
\u041c\u043e\u0434\u0435\u043b\u0438 \u043d\u0435 \u0438\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u0443\u044e\u0442 \u0434\u0440\u0443\u0433 \u0434\u0440\u0443\u0433\u0430 \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e \u2014 \u0441\u0432\u044f\u0437\u0438 \u0437\u0430\u0434\u0430\u044e\u0442\u0441\u044f \u0441\u0442\u0440\u043e\u043a\u0430\u043c\u0438 \u0438\u043c\u0451\u043d \u0442\u0430\u0431\u043b\u0438\u0446.\n\"\"\"

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
