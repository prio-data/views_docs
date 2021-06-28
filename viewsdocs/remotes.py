from typing import Tuple
import os
import logging
import json
from json.decoder import JSONDecodeError

import aiohttp
from pydantic import ValidationError

import views_schema as schema
from .exceptions import RemoteError

logger = logging.getLogger(__name__)

class RemoteContentApi():
    def __init__(self, base_url, client: aiohttp.ClientSession):
        self._base_url = base_url
        self._client = client

    async def _fetch(self,url)-> Tuple[str,int]:
        logging.critical(url)
        url = url.strip("/")
        logger.debug("Fetching %s", url)
        async with self._client.get(url) as response:
            content = await response.text()
            logger.debug("Got %s (%s chr)", url, str(len(content)))
            return content, response.status

    async def _fetch_entry(self, url):
        content, status_code = await self._fetch(url)
        try:
            return schema.DocumentationEntry(**json.loads(content))
        except (JSONDecodeError, ValidationError) as err:
            raise RemoteError(
                    message = f"Remote {url} returned bad data",
                    data = content,
                    status_code = status_code
                    ) from err

    async def get(self, path: str)-> schema.DocumentationEntry:
        url = os.path.join(self._base_url, path)
        entry = await self._fetch_entry(url)
        return entry

    async def list(self)-> schema.DocumentationEntry:
        entry = await self.get("")
        return entry
