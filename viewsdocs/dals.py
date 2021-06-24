
import logging
from collections import namedtuple
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schema

logger = logging.getLogger(__name__)

class AsyncDal(ABC):
    @property
    @abstractmethod
    def __db_model__(self)-> Any:
        pass

    def __init__(self, session: AsyncSession):
        """
        A data access layer, which is used to get and set data in a remote database.

        Args:
            session (AsyncSession): A session instance for database access
        """
        self._session = session

    async def _new(self, primary_key):
        instance = self.__db_model__(*primary_key)
        self._session.add(instance)
        self._session.commit()
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

class PageDal(AsyncDal):
    __db_model__ = models.DocumentationPage

    def __init__(self, session: AsyncSession,
            category: str = "doc", prefix: str = ""):
        """
        A data access layer that maps paths to documentation pages.
        Subclasses cover different domains.

        Args:
            session (AsyncSession): A session instance for database access
            category(Optional[str]): A category which groups fetched / added pages
            prefix(Optional[Callable[[str],str]]): A callable which can be used to
                prefix the category argument.
        """
        self._category = category
        self._prefix = prefix
        super().__init__(session)

    @property
    def __category_name__(self):
        return self._prefix +"_"+self._category if self._prefix else self._category

    async def add(self, path: str, content: str, author: Optional[str] = None)-> None:
        """
        Add content associated with a path, overwriting existing content if present.

        Args:
            path(str): The path to write to
            content(str): The content to write
            author(Optional[str]): The author of the content

        Returns:
            None
        """
        primary_key = self._path_to_pk(path)

        logger.debug("Annotating %s (%s chr)",
                primary_key,
                str(len(content)))

        page = await self._get_or_create(primary_key)
        page.content = content
        page.last_edited = datetime.now()
        if author:
            page.author = author
        return page

    async def get(self, path: str)-> schema.DocumentationPageDetail:
        """
        Get the documentation data associated with a path.

        Args:
            path(str): The path associated with desired content

        Returns:
            schema.DocumentationPageDetail
        """

        page = await self._get(self._path_to_pk(path))
        if page:
            return page.detail_schema()
        else:
            return None

    async def list(self) -> List[schema.DocumentationPage]:
        """
        Gets a list of documentation pages associated with the class category.

        Returns:
            List[schema.DocumentationPage]
        """
        statement = (
                select(self.__db_model__)
                .where(self.__db_model__.category == self.__category_name__)
            )
        result = await self._session.execute(statement)
        return [page.list_schema() for page in result.scalars().all()]

    def _path_to_pk(self, path)-> PageDalPk:
        """
        Converts a path to a database key,  which can be used to get or set content in the database.
        """
        *_, name = path.split("/")
        return PageDalPk(name, self.__category_name__)
