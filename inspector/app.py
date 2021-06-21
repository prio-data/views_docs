
from fastapi import FastAPI, Response
from . import crud, remotes

# ...https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08...

Base = declarative_base()

@app.get("/{path: path}")
def get_doc(path: str):
    path = Path(path)
    return content

@app.post("/{path: path}")
def post_doc(path: str):
    return Response(status_code = 201)
