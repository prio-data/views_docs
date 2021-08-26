
import logging
from environs import Env

logger = logging.getLogger(__name__)

env = Env()
config = env

REMOTES = {
        "tables": config("BASE_DATA_RETRIEVER_URL") + "/tables",
        "columns": config("BASE_DATA_RETRIEVER_URL") + "/tables",
        "transforms": config("TRANSFORMER_URL") + "/transforms",
    }

def remote(kind: str):
    return REMOTES.get(kind)
