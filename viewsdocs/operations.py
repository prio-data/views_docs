import logging
from typing import Optional, List
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
import views_schema as schema
from . import dals, remotes

logger = logging.getLogger(__name__)

class DocumentationOperations():
    """
    A set of operations for fetching documentation data from both the
    documentation database and endpoints exposed by remote services.
    """
    def __init__(self,
            base_url: str,
            session: AsyncSession,
            http_client: ClientSession,
            name: str = "",
            category_name: str = "doc"):

        self._name = name

        self._dal = dals.PageDal(
                session,
                category_name,
            )

        self._api = remotes.RemoteContentApi(
                base_url,
                http_client,
            )

    async def get(self, path: str) -> schema.ViewsDoc:
        data, documentation = await asyncio.gather(
                self._api.get(path),
                self._dal.get(path)
                )
        return schema.ViewsDoc(
                    proxied = data,
                    documentation = documentation
                )

    async def add(self, posted: schema.ViewsDoc, author: Optional[str] = None) -> None:
        await self._dal.add(self._name, posted.content, author)

    async def list(self) -> List[schema.DocumentationEntry]:
        pages = await self._api.list()
        return pages
