
import sys
import logging
from typing import Protocol, Optional, List
from aiohttp import ClientSession
from fastapi import FastAPI, Depends, Response
import views_schema as schema
from . import operations, models, db, settings, __version__, exceptions

app = FastAPI()

logging.basicConfig(level = getattr(logging, settings.config.str("LOG_LEVEL", "WARNING").upper()))

class CrudOperations(Protocol):
    async def add(self, key:str, to_add: schema.PostedDocumentationPage)-> None:
        """
        Add posted data to the documentation database, under the provided key
        """
    async def get(self, key:str) -> models.DocumentationPage :
        """
        Get documentation pertaining to the key
        """
    async def list(self) -> List[schema.DocumentationPageListEntry]:
        """
        List available documentation
        """

async def get_ops(kind:str, location:str) -> Optional[CrudOperations]:
    async with ClientSession() as http_client:
        async with db.Session() as session:
            base_url = settings.remote(kind)
            if base_url is None:
                yield None

            location = location.split("/")
            base_url += "/".join(location[:-1])
            category_name = "_".join([kind] + location)
            doc_name = "".join(location[-1:])

            yield operations.DocumentationOperations(
                    base_url, session, http_client,
                    name = doc_name,
                    category_name = category_name
                )

@app.get("/")
def handshake():
    return {"version":__version__}

@app.get("/docs/{kind:str}{location:path}")
async def get(kind: str, ops:Optional[CrudOperations] = Depends(get_ops))-> schema.ViewsDoc:
    if ops is None:
        return Response(f"Could not find url for {kind}",status_code = 404)
    try:
        pages = await ops.get()
    except exceptions.RemoteError as re:
        if re.status_code == 404:
            return Response(str(re), status_code = 404)
        else:
            raise re
    return pages

@app.post("/docs/{kind:str}{location:path}")
async def post(
        posted: schema.PostedDocumentationPage,
        ops:Optional[CrudOperations] = Depends(get_ops)) -> schema.ViewsDoc:
    if ops is None:
        return Response(status_code = 404)
    await ops.add(posted)
    return Response(status_code = 201)
