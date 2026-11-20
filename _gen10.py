# -*- coding: utf-8 -*-
import pathlib
ROOT = pathlib.Path(r"D:\Makefab\projects\vernicredit\backend")
FILES = {}

FILES[r"alembic.ini"] = """# \u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f Alembic.\n# \u0410\u0434\u0440\u0435\u0441 \u0411\u0414 \u0431\u0435\u0440\u0451\u0442\u0441\u044f \u0438\u0437 DATABASE_URL (\u0441\u043c. alembic/env.py), \u043d\u0435 \u0438\u0437 \u044d\u0442\u043e\u0433\u043e \u0444\u0430\u0439\u043b\u0430.\n\n[alembic]\nscript_location = alembic\nprepend_sys_path = .\nversion_path_separator = os\n\n[loggers]\nkeys = root,sqlalchemy,alembic\n\n[handlers]\nkeys = console\n\n[formatters]\nkeys = generic\n\n[logger_root]\nlevel = WARN\nhandlers = console\nqualname =\n\n[logger_sqlalchemy]\nlevel = WARN\nhandlers =\nqualname = sqlalchemy.engine\n\n[logger_alembic]\nlevel = INFO\nhandlers =\nqualname = alembic\n\n[handler_console]\nclass = StreamHandler\nargs = (sys.stderr,)\nlevel = NOTSET\nformatter = generic\n\n[formatter_generic]\nformat = %(levelname)-5.5s [%(name)s] %(message)s\ndatefmt = %H:%M:%S\n"""

FILES[r"alembic\env.py"] = """# -*- coding: utf-8 -*-
\"\"\"Alembic \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u0435.\n\n\u0410\u0434\u0440\u0435\u0441 \u0411\u0414 \u0431\u0435\u0440\u0451\u0442\u0441\u044f \u0438\u0437 DATABASE_URL (\u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f), \u0434\u0435\u0444\u043e\u043b\u0442 \u2014 sqlite:///./vernicredit.db.\n\u0422\u0430\u043a\u0436\u0435 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442\u0441\u044f \u0448\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u0441\u043f\u043e\u0441\u043e\u0431 Alembic: \u043f\u0435\u0440\u0435\u0434\u0430\u0442\u044c sqlalchemy.url \u0432 \u0432\u044b\u0437\u043e\u0432\u0435.\n\"\"\"

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# \u041a\u043e\u0440\u0435\u043d\u044c backend/ \u0432 sys.path, \u0447\u0442\u043e\u0431\u044b \u0438\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c app.*
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.db.base import Base  # noqa: E402
import app.models  # noqa: E402,F401  \u2014 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u043c\u043e\u0434\u0435\u043b\u0435\u0439 \u0432 Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# \u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442: \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0438\u0437 \u0432\u044b\u0437\u043e\u0432\u0430 (-x sqlalchemy.url=...) > DATABASE_URL > \u0434\u0435\u0444\u043e\u043b\u0442.\nDATABASE_URL = config.get_main_option("sqlalchemy.url") or os.getenv(
    "DATABASE_URL", "sqlite:///./vernicredit.db"
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    \"\"\"\u041e\u0444\u043b\u0430\u0439\u043d-\u0440\u0435\u0436\u0438\u043c: \u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f SQL \u0431\u0435\u0437 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043a \u0411\u0414.\"\"\"
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=DATABASE_URL.startswith("sqlite"),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    \"\"\"\u041e\u043d\u043b\u0430\u0439\u043d-\u0440\u0435\u0436\u0438\u043c: \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a \u0411\u0414.\"\"\"
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=connection.dialect.name == "sqlite",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

FILES[r"alembic\script.py.mako"] = """\"\"\"${message}\n\nRevision ID: ${up_revision}\nRevises: ${down_revision | comma,n}\nCreate Date: ${create_date}\n\"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""

for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("WROTE", p)
