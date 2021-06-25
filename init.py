
import uvicorn
from ensure_certs import ensure_certs
from viewsdocs.app import app

if __name__ == "__main__":
    ensure_certs()
    uvicorn.run(app, host="0.0.0.0", port="80")
