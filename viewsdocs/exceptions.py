from typing import Optional

class RemoteError(ValueError):
    def __init__(self,
            data: Optional[any] = None,
            message: str = "",
            status_code: Optional[int] = None):

        if data:
            message += " Received " + str(data)
        if status_code:
            message += f" with status_code {status_code}"

        super().__init__(message)
