# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"app\db\__init__.py"] = """# -*- coding: utf-8 -*-
\"\"\"\u0421\u043b\u043e\u0439 \u0434\u043e\u0441\u0442\u0443\u043f\u0430 \u043a \u0431\u0430\u0437\u0435 \u0434\u0430\u043d\u043d\u044b\u0445.\"\"\"

from app.db.base import Base
from app.db.session import SessionLocal, engine, get_db

__all__ = ["Base", "SessionLocal", "engine", "get_db"]
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
