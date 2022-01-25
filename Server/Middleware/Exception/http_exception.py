from fastapi.responses import JSONResponse


class IPBanException(Exception):
    def __init__(self, message: str):
        self.message = message

    async def error(self):
        return JSONResponse(status_code=500, content={"message": f"{self.message}"})

