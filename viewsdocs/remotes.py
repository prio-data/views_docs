from typing import List
import os
import logging
import re
from urllib.parse import urlparse, urlunparse
import json
from abc import ABC
import aiohttp
from . import schema

logger = logging.getLogger(__name__)

class RemoteContentApi(ABC):
    __list_key__ = "data"

    def __init__(self, base_url, client: aiohttp.ClientSession):
        self._base_url = base_url
        self._client = client

    def _remote_to_local_url(self, url: str)-> str:
        return url

    def _local_to_remote_url(self, url: str)-> str:
        return url

    async def _fetch(self,url):
        logging.critical(url)
        url = self._local_to_remote_url(url)
        logger.debug("Fetching %s", url)
        async with self._client.get(url) as response:
            content = await response.text()
            logger.debug("Got %s (%s chr)", url, str(len(content)))
            return content

    async def _fetch_json(self,url):
        content = await self._fetch(url)
        if content:
            return json.loads(content)
        else:
            return dict()

    async def list(self) -> List[schema.RemoteLocation]:
        raw_data = await self._fetch_json(self._base_url)
        try:
            listed_data = raw_data[self.__list_key__]
        except KeyError:
            return []

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

    def _remote_to_local_url(self, url):
        url = re.sub(r"/(?=(?:[^.]+\.?){2}$)",".",url)
        return url

    def _local_to_remote_url(self, url):
        logging.critical(url)
        parsed = urlparse(url)
        path = re.sub(r"\.","/",parsed.path,1)
        url = urlunparse(parsed._replace(path = path) )
        logging.critical(url)
        return url

    async def list(self):
        data = await super().list()
        for entry in data:
            remote_url = entry["level_of_analysis"]+"/"+entry["namespace"]+ "." +entry["name"]
            entry["path"] = self._remote_to_local_url(remote_url)
        return data
