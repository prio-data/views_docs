import os
import asyncio
import logging
from typing import Dict, Tuple, Optional
import json
from abc import ABC
from sqlalchemy import orm
import aiohttp
from . import dals, exceptions

logger = logging.getLogger(__name__)

class RemoteContentApi(ABC):
    __list_key__ = "data"
    __annotation_key__ = "doc"

    __annotation_category__: Optional[str] = "documentation"

    def __init__(self, base_url, client: aiohttp.ClientSession, session: orm.Session):
        self._base_url = base_url
        self._client = client
        self._session = session

        if self.__annotation_category__ is not None:
            self._dal = dals.PageDal(self._session)
        else:
            self._dal = None

    async def _fetch(self,url):
        logger.debug("Fetching %s", url)
        async with self._client.get(url) as response:
            content = await response.text()
            logger.debug("Got %s (%s chr)", url, str(len(content)))
            return content

    async def _fetch_json(self,url):
        content = await self._fetch(url)
        return json.loads(content)

    async def list(self):
        raw_data = await self._fetch_json(self._base_url)
        try:
            listed_data = raw_data[self.__list_key__]
        except KeyError:
            raise exceptions.RemoteError(raw_data,
                    f"Could not index with {self.__list_key__} to get list of values.")

        data = [e if not isinstance(e,str) else {"path":e} for e in listed_data]

        return data

    async def show(self, key: str):
        url = os.path.join(self._base_url, key)
        data_request = self._fetch_json(url)

        if self._dal:
            logger.debug("Getting annotation for %s - %s",
                    self.__annotation_category__, key)
            annotation_request = self._dal.content(self.__annotation_category__, key)
        else:
            annotation = ""

        data, annotation = await asyncio.gather(data_request, annotation_request)

        #data = await data_request
        #annotation = await annotation_request
        data[self.__annotation_key__] = annotation

        return data

class DatabaseTableApi(RemoteContentApi):
    __list_key__ = "tables"
    __annotation_category__ = None

    async def show(self, key:str):
        """
        Returns a column API rather than just the column name
        """
        return DatabaseColumnApi(self._base_url+"/"+key, self._client, self._session)

class DatabaseColumnApi(RemoteContentApi):
    __list_key__ = "columns"

    __annotation_dal__ = dals.PageDal
    __annotation_category__ = "column"

class TransformsApi(RemoteContentApi):
    __list_key__ = "transforms"

    __annotation_dal__ = dals.PageDal
    __annotation_category__ = "transform"

    async def list(self):
        data = await super().list()
        for entry in data:
            entry["path"] = entry["level_of_analysis"]+"/"+entry["namespace"]+ "." +entry["name"]
        return data

class RemotesRegistry:
    def __init__(self):
        self.remotes: Dict[str, Tuple[RemoteContentApi, str]] = dict()

    def register(self, name: str, remote_url: str, api_class = RemoteContentApi):
        self.remotes[name] = (remote_url, api_class)

    def api(self, name, client: aiohttp.ClientSession, session: orm.Session):
        url, api_class = self.remotes[name]
        return api_class(url, client, session)
