
from typing import List,Any,Dict
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import remotes, models

class DocumentationSource(ABC):
    __db_model__ = models.DocumentationPage

    @property
    @abstractmethod
    def __remotes_name__(self)-> str:
        pass

    @property
    @abstractmethod
    def __db_category__(self)-> str:
        pass

    def __init__(self, remotes_registry: remotes.RemotesRegistry, session: AsyncSession):
        self.remotes_registry = remotes_registry
        self.session = session

    @abstractmethod
    async def list(self) -> List[Any]:
        pass

    @abstractmethod
    async def show(self, key: str)-> Dict[Any,Any]:
        pass

    async def get_annotation(self, key: str):
        statement = (
                select(self.__db_model__)
                .filter(self.__db_model__.category == self.__db_category__)
                .get(key)
            )
        return await self.session.execute(statement)

class ColumnDocumentation(DocumentationSource):
    __db_category__ = "column"
    __remotes_name__ = "docs"

    async def list(self) -> List[Any]:
        return []

    async def show(self, key: str):
        return {}
