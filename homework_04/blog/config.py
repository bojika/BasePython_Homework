import os

SQLA_ECHO = True


# ### dialect[+driver]://user:password@host/dbname
SQLA_CONN_SYNC_URI = os.environ.get("SQLA_CONN_SYNC_URI") or\
                     "postgresql+pg8000://pguser:pgpasswd@localhost/blog_project"

# SQLA_CONN_ASYNC_URI = os.environ.get("SQLA_CONN_ASYNC_URI") or\
#                       "postgresql+asyncpg://user:password@localhost/blog_project"
SQLA_CONN_ASYNC_URI = os.environ.get("SQLA_CONN_ASYNC_URI") or\
                     "sqlite+aiosqlite:///./h04_db.sqlite"

