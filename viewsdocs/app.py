
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from fastapi import FastAPI, Depends, Response
from . import operations, schema, db, settings, __version__

app = FastAPI()

async def get_session()-> AsyncSession:
    async with db.Session() as session:
        yield session

async def get_http_client()-> ClientSession:
    async with ClientSession() as http_client:
        yield http_client

@app.get("/")
def handshake():
    return {"version": __version__}

@app.get("/tables/{table_name:str}")
async def get_table_doc(
        table_name: str,
        session = Depends(get_session), client = Depends(get_http_client)):
    table_operations = operations.TableDocumentationOperations(
            settings.remote("tables"), session, client
            )
    data = await table_operations.get(table_name)
    return data

@app.post("/tables/{table_name:str}")
async def post_table_doc(
        table_name: str,
        posted: schema.PostedDocumentation,
        session = Depends(get_session), client = Depends(get_http_client)):
    table_operations = operations.TableDocumentationOperations(
            settings.remote("tables"), session, client
            )
    data = await table_operations.add(table_name, posted.content)
    await session.commit()
    return data

@app.get("/tables/{table_name:str}/{column_name:str}")
async def get_column_doc(
        table_name: str, column_name: str,
        session = Depends(get_session), client = Depends(get_http_client)):
    column_operations = operations.ColumnDocumentationOperations(
            settings.remote("tables"), session, client, table_name
            )
    data = await column_operations.get(table_name+"/"+column_name)
    return data

@app.post("/tables/{table_name:str}/{column_name:str}")
async def post_column_doc(
        table_name: str, column_name: str,
        posted: schema.PostedDocumentation,
        session = Depends(get_session), client = Depends(get_http_client)):
    column_operations = operations.ColumnDocumentationOperations(
            settings.remote("tables"), session, client, table_name
            )
    data = await column_operations.add(table_name+"/"+column_name, posted.content)
    await session.commit()
    return data
