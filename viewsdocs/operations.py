import re
from typing import Optional, Union
import asyncio
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from . import dals, remotes, schema

class DocumentationOperations(ABC):
    __doc_key__ = "doc"
    __path_length__ = 1

    @property
    @abstractmethod
    def __api_class__(self)-> remotes.RemoteContentApi:
        pass

    @property
    @abstractmethod
    def __dal_class__(self)-> dals.Dal:
        pass

    @property
    def __path_regex__(self):
        return "^(?:[^/]+/?){" + str(self.__path_length__) + "}$"

    def __init__(self, base_url: str, session: AsyncSession, http_client: ClientSession):
        self._dal = self.__dal_class__(session)
        self._api = self.__api_class__(base_url, http_client)

    def validate_path(self, path: str):
        assert re.search(self.__path_regex__, path) is not None

    async def get(self, path: str) -> schema.Documentation:
        self.validate_path(path)
        data, documentation = await asyncio.gather(
                self._api.get(path),
                self._dal.get(path)
                )
        return schema.Documentation(
                    proxied = data,
                    documentation = documentation
                )

    async def add(self, path: str, content: str, author: Optional[str] = None) -> None:
        self.validate_path(path)
        await self._dal.add(path, content, author)

class TableDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.TableApi
    __dal_class__ = dals.TablePagesDal

class ColumnDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.ColumnApi
    __dal_class__ = dals.ColumnPagesDal
    __path_length__ = 2
    def __init__(self, base_url: str, session: AsyncSession, http_client: ClientSession, table_name: str):
        self._dal = self.__dal_class__(session, table_name)
        self._api = self.__api_class__(base_url, http_client)

class TransformDocumentationOperations(DocumentationOperations):
    __api_class__ = remotes.TransformApi
    __dal_class__ = dals.TransformPagesDal
