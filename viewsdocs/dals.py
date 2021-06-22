
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models

logger = logging.getLogger(__name__)

class Dal(ABC):
    @property
    @abstractmethod
    def __db_model__(self)-> Any:
        pass

    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def _new(self, primary_key):
        pass

    async def _get_or_create(self, primary_key) -> Optional[Any]:
        try:
            instance = await self._get(primary_key)
            assert instance is not None
        except AssertionError:
            instance = await self._new(primary_key)
        return instance

    async def _get(self, primary_key):
        instance = await self._session.get(self.__db_model__, primary_key)
        return instance

    async def exists(self, primary_key):
        something = await self._get(primary_key)
        return something is not None

class PageDal(Dal):
    __db_model__ = models.DocumentationPage

    async def _new(self, primary_key):
        category, name = primary_key
        page = self.__db_model__(category, name)
        self._session.add(page)
        return page

    async def add(self, category: str, name: str, content: str, author: Optional[str] = None):
        """
        Add content associated with category, overwriting existing content if present.
        """
        logger.debug("Annotating %s - %s (%s chr)", category, name, str(len(content)))
        page = await self._get_or_create((category, name))
        page.content = content
        page.last_edited = datetime.now()
        if author:
            page.author = author
        return page

    async def show(self, category: str, name: str)-> models.DocumentationPageDetailSchema:
        page = await self._get((category, name))
        if page:
            return page.detail_schema()
        else:
            return None

    async def content(self, category: str, name: str)-> str:
        logger.debug("Getting annotation for %s - %s", category, name)
        page = await self.show(category, name)
        content = page.content if page else ""
        logger.debug("Got annotation for %s - %s (%s chr)", category, name, str(len(content)))
        return content

    async def list(self, category: Optional[str] = None)-> List[models.DocumentationPageSchema]:
        """
        Gets a list of documentation pages, optionally filtered on category
        """
        statement = select(self.__db_model__)
        if category:
            statement = statement.where(self.__db_model__.category == category)
        result = await self._session.execute(statement)
        return [page.list_schema() for page in result.scalars().all()]
