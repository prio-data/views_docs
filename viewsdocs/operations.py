from typing import Optional, List
import asyncio
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from . import dals, remotes, schema

class DocumentationOperations(ABC):
    """
    A set of operations for fetching documentation data from both the
    documentation database and endpoints exposed by remote services.
    """
    __doc_key__ = "doc"
    __category_name__ = "doc"
    __prefix__ = ""

    @property
    @abstractmethod
    def __api_class__(self)-> remotes.RemoteContentApi:
        pass

    def __init__(self, base_url: str, session: AsyncSession, http_client: ClientSession):
        self._dal = dals.PageDal(session, self.__category_name__, prefix = self.__prefix__)
        self._api = self.__api_class__(base_url, http_client)

    async def get(self, path: str) -> schema.AnnotatedProxiedDocumentation:
        data, documentation = await asyncio.gather(
                self._api.get(path),
                self._dal.get(path)
                )
        return schema.AnnotatedProxiedDocumentation(
                    proxied = data,
                    documentation = documentation
                )

    async def add(self, path: str, content: str, author: Optional[str] = None) -> None:
        await self._dal.add(path, content, author)

    async def list(self) -> List[schema.RemoteLocation]:
        pages = await self._api.list()
        return pages

class TableDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.TableApi
    __category_name__ = "tables"

class TransformDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.TransformApi
    __category_name__ = "transforms"

class ColumnDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.ColumnApi
    __prefix__ = "tables"

    def __init__(self, base_url: str,
            session: AsyncSession, http_client: ClientSession,
            table_name: str):
        self.__category_name__ = table_name
        super().__init__(base_url, session, http_client)
