
import logging
from environs import Env

logger = logging.getLogger(__name__)

env = Env()

LOG_LEVEL               = env.str("LOG_LEVEL", "WARNING").upper()

DB_HOST                 = env.str("DOCS_DB_HOST", "127.0.0.1")
DB_PORT                 = env.str("DOCS_DB_PORT", "5432")
DB_USER                 = env.str("DOCS_DB_USER", "postgres")
DB_NAME                 = env.str("DOCS_DB_NAME", "postgres")
DB_PASSWORD             = env.str("DOCS_DB_PASSWORD", "")
DB_SSL                  = env.bool("DOCS_DB_SSL", True)

BASE_DATA_RETRIEVER_URL = env.str("BASE_DATA_RETRIEVER_URL")
TRANSFORMER_URL         = env.str("TRANSFORMER_URL")

REMOTES = {
        "tables":     BASE_DATA_RETRIEVER_URL + "/tables",
        "columns":    BASE_DATA_RETRIEVER_URL + "/tables",
        "transforms": TRANSFORMER_URL + "/transforms",
    }

def remote(kind: str):
    return REMOTES.get(kind)
