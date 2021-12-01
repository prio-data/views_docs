import ssl
import os
import time
from datetime import datetime
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncpg

from . import settings

logger = logging.getLogger(__name__)

connect_args = {}

if settings.DB_SSL:
    cert_path = lambda x: os.path.expanduser(f"~/.postgresql/{x}")
    logger.critical("READY")

    cert_files = ["postgresql.key","postgresql.crt","root.crt"]

    start = datetime.now()

    while not all([os.path.exists(cert_path(x)) for x in cert_files]):
        time.sleep(1)
        logger.info(f"Waiting for certs ({(datetime.now() - start).seconds} seconds have passed)")


    ssl_context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH,
            cafile = cert_path("root.crt")
            )

    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_OPTIONAL
    ssl_context.load_cert_chain(
            cert_path("postgresql.crt"),
            keyfile = cert_path("postgresql.key"),
            )

    connect_args.update({"ssl": ssl_context})

user_string = settings.DB_USER + ":" + settings.DB_PASSWORD if settings.DB_PASSWORD else settings.DB_USER

connection_string = (
            "postgresql+asyncpg://"
            f"{user_string}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )

engine = create_async_engine(connection_string, connect_args = connect_args)
Session = sessionmaker(bind = engine, class_ = AsyncSession)
