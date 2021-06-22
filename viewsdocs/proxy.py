
import aiohttp
from . import crud

class AnnotatedProxy:
    def __init__(self, remotes):
        self.remotes = remotes
        self._session = aiohttp.ClientSession()

    async def proxy(host_name, path_name):

        async with aiohttp.ClientSession() as session

    async def _fetch(
