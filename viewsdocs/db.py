
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .settings import config

cert_path = lambda f: os.path.join(os.path.expanduser("~/.postgresql"),f)

DB_URL = (f"postgresql+asyncpg://{config('DB_USER')}@{config('DB_HOST')}/{config('DOCS_DB_NAME')}"
    f"?sslcert={cert_path('views.crt')}"
    f"&sslkey={cert_path('views.key')}"
    "&ssl=require"
    )

engine = create_async_engine(DB_URL)
Session = sessionmaker(bind = engine, class_ = AsyncSession)
