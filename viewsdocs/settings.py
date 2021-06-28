
from functools import lru_cache
from azure.identity import DefaultAzureCredential
from environs import Env
from fitin import views_config, seek_config

env = Env()

remote_config = views_config(env.str("KEY_VAULT_URL"), DefaultAzureCredential())

@lru_cache(maxsize=None)
def config(key: str):
    return seek_config(resolvers = [
            remote_config
        ])(key)

def remote(kind: str):
    remotes = {
            "tables": config("BASE_DATA_RETRIEVER_URL") + "/tables",
            "columns": config("BASE_DATA_RETRIEVER_URL") + "/tables",
            "transforms": config("TRANSFORMER_URL") + "/transforms",
        }
    return remotes.get(kind)

