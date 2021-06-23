
import logging
from collections import namedtuple
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schema

logger = logging.getLogger(__name__)

class Dal(ABC):
    @property
    @abstractmethod
    def __db_model__(self)-> Any:
        pass

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _new(self, primary_key):
        instance = self.__db_model__(*primary_key)
        self._session.add(instance)
        return instance

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
        instance = await self._get(primary_key)
        return instance is not None


PageDalPk = namedtuple("PageDalPk",("name","category"))

class PageDal(Dal):
    __db_model__ = models.DocumentationPage
    __category_name__ = "doc"

    async def add(self, path: str, content: str, author: Optional[str] = None):
        """
        Add content associated with category, overwriting existing content if present.
        """
        primary_key = self.path_to_pk(path)

        logger.debug("Annotating %s (%s chr)",
                primary_key,
                str(len(content)))

        page = await self._get_or_create(primary_key)
        page.content = content
        page.last_edited = datetime.now()
        if author:
            page.author = author
        return page

    async def get(self, path: str)-> schema.DocumentationPageDetailSchema:
        page = await self._get(self.path_to_pk(path))
        if page:
            return page.detail_schema()
        else:
            return None

    async def content(self, path: str)-> str:
        page = await self.get(path)
        content = page.content if page else ""
        return content

    async def list(self) -> List[schema.DocumentationPageSchema]:
        """
        Gets a list of documentation pages, optionally filtered on category
        """
        statement = (
                select(self.__db_model__)
                .where(self.__db_model__.category == self.__category_name__)
            )
        result = await self._session.execute(statement)
        return [page.list_schema() for page in result.scalars().all()]

    def path_to_pk(self, path)-> PageDalPk:
        *_, name = path.split("/")
        return PageDalPk(name, self.__category_name__)

class TablePagesDal(PageDal):
    __category_name__ = "table"

class TransformPagesDal(PageDal):
    __category_name__ = "transforms"

class ColumnPagesDal(PageDal):
    def __init__(self, session: AsyncSession, table_name: str):
        self._table_name = table_name
        super().__init__(session)

    @property
    def __category_name__(self):
        return "table_" + self._table_name
