"""
Fetches database certificates
"""
import logging
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)

def ensure_certs():
    to_get = [
        ("views-root-cert", "views-root.crt"),
        ("views-cert", "views.crt"),
        ("views-key", "views.key"),
    ]

    client = SecretClient(os.getenv("KEY_VAULT_URL"),DefaultAzureCredential())

    for secret_name, file_name in to_get:
        folder = os.path.expanduser("~/.postgresql")
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass
        else:
            logger.warning("Made .postgresql dir")

        path = os.path.join(folder,file_name)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(client.get_secret(secret_name).value)
        else:
            logger.warning("Cert %s already exists at %s", secret_name, file_name)

if __name__ == "__main__":
    ensure_certs()
