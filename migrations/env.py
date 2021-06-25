import asyncio
from logging.config import fileConfig
from alembic import context
from viewsdocs.models import Base
from viewsdocs.db import engine

config = context.config

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
                connection = connection, target_metadata = target_metadata
            )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

asyncio.run(run_migrations_online())
