
class RemoteError(ValueError):
    def __init__(self, data, message):
        message = message + " Received " + str(data)
        super().__init__(message)

