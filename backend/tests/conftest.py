"""Pytest bootstrap shared by every test module.

Sets a placeholder DATABASE_URL before any `app.*` import path can run,
because `app.core.database` instantiates a SQLAlchemy async engine eagerly
at import time and refuses an empty URL. Production deployments override
this through the real `.env`; we only need a syntactically valid value here.
"""

import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://placeholder/db")
