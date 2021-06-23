
BASE_DATA_RETRIEVER_URL = "http://0.0.0.0:8003/tables"
TRANSFORMS_URL = "http://0.0.0.0:8002/transforms"

def remote(kind: str):
    remotes = {
            "tables": BASE_DATA_RETRIEVER_URL,
            "columns": BASE_DATA_RETRIEVER_URL,
            "transforms": TRANSFORMS_URL,
        }
    return remotes[kind]
