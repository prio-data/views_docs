
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from . import models

sync_engine = create_engine("sqlite:///tmp.sqlite")
models.Base.metadata.create_all(sync_engine)

engine = create_async_engine("sqlite+aiosqlite:///tmp.sqlite")
Session = sessionmaker(bind = engine, class_ = AsyncSession)
