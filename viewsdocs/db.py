
import os
import ssl

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from asyncpg import connect

from .settings import config

cert_path = lambda f: os.path.join(os.path.expanduser("~/.postgresql"),f)

DB_URL = (f"postgresql+asyncpg://{config('DB_USER')}@{config('DB_HOST')}/{config('DOCS_DB_NAME')}")

ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile = cert_path("views-root.crt")
        )

ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_cert_chain(
        cert_path("views.crt"),
        keyfile = cert_path("views.key"),
        )

engine = create_async_engine(DB_URL,connect_args = {"ssl": ssl_context})
Session = sessionmaker(bind = engine, class_ = AsyncSession)
