import os
import logging
from typing import Dict, Tuple
import json
from abc import ABC
from sqlalchemy import orm
import aiohttp
from . import exceptions

logger = logging.getLogger(__name__)

class RemoteContentApi(ABC):
    __list_key__ = "data"

    def __init__(self, base_url, client: aiohttp.ClientSession):
        self._base_url = base_url
        self._client = client

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

    async def get(self, key: str):
        url = os.path.join(self._base_url, key)
        data = await self._fetch_json(url)
        return data

class TableApi(RemoteContentApi):
    __list_key__ = "tables"

class ColumnApi(RemoteContentApi):
    __list_key__ = "columns"

class TransformApi(RemoteContentApi):
    __list_key__ = "transforms"

    async def list(self):
        data = await super().list()
        for entry in data:
            entry["path"] = entry["level_of_analysis"]+"/"+entry["namespace"]+ "." +entry["name"]
        return data
