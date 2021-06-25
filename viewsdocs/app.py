
import asyncio
from typing import Protocol, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from fastapi import FastAPI, Depends, Response
from . import operations, schema, models, db, settings, __version__

app = FastAPI()

class CrudOperations(Protocol):
    async def add(self, key:str, to_add:schema.PostedDocumentation)-> None:
        """
        Add posted data to the documentation database, under the provided key
        """
    async def get(self, key:str) -> models.DocumentationPage :
        """
        Get documentation pertaining to the key
        """
    async def list(self) -> List[schema.DocumentationPage]:
        """
        List available documentation
        """

async def get_ops(
        kind:str,
        name:Optional[str] = None,
        sub_name:Optional[str] = None)-> Optional[CrudOperations]:
    async with ClientSession() as http_client:
        async with db.Session() as session:
            base_url = settings.remote(kind)
            args = [base_url, session, http_client]

            if kind == "tables":
                if sub_name is None:
                    ops = operations.TableDocumentationOperations
                else:
                    args.append(name)
                    ops = operations.ColumnDocumentationOperations
            elif kind == "transforms":
                ops = operations.TransformDocumentationOperations
            elif kind == "columns":
                args.append(name)
            else:
                yield None
            yield ops(*args)

@app.get("/")
def handshake():
    return {"version":__version__}

@app.get("/docs/{kind:str}")
async def list(ops:Optional[CrudOperations] = Depends(get_ops)):#-> List[schema.DocumentationPage]:
    if ops is None:
        return Response(status_code = 404)
    pages = await ops.list()
    return pages

@app.get("/docs/{kind:str}/{name:str}")
async def show(name:str, ops:Optional[CrudOperations] = Depends(get_ops)
        ) -> schema.AnnotatedProxiedDocumentation:
    if ops is None:
        return Response(status_code = 404)
    page = await ops.get(name)
    return page

@app.post("/docs/{kind:str}/{name:str}")
async def post(name:str, posted:schema.PostedDocumentation,
        ops:Optional[CrudOperations] = Depends(get_ops)) -> Response:
    if ops is None:
        return Response(status_code = 404)
    await ops.add(name, posted)
    return Response(status_code = 201)

@app.get("/docs/{kind:str}/{name:str}/{sub_name:str}")
async def show_sub(name:str, sub_name:str, ops:Optional[CrudOperations] = Depends(get_ops)):
    if ops is None:
        return Response(status_code = 404)
    page = await ops.get(name+"/"+sub_name)
    return page

@app.post("/docs/{kind:str}/{name:str}/{sub_name:str}")
async def post_sub(name:str, sub_name:str, posted:schema.PostedDocumentation,
        ops:Optional[CrudOperations] = Depends(get_ops)) -> Response:
    if ops is None:
        return Response(status_code = 404)
    await ops.add(name+"/"+sub_name, posted)
    return Response(status_code = 201)
