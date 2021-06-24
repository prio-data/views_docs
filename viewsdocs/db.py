

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .settings import config

DB_URL = (f"postgresql+asyncpg://{config('DB_USER')}@{config('DB_HOST')}/{config('DOCS_DB_NAME')}"
    f"?sslcert={config('SSLCERT')}"
    f"&sslkey={config('SSLKEY')}"
    f"&sslrootcert={config('SSLROOTCERT')}"
    "&ssl=require"
    )

engine = create_async_engine(DB_URL, echo = True)
Session = sessionmaker(bind = engine, class_ = AsyncSession)
