import re
from pydantic import BaseModel


class HistoryPost(BaseModel):
    upImg: str

    async def base64_generator(self):
        base64_data = re.sub('^data:image/.+;base64,', '', self.upImg)
        byte_base64_data = base64_data.encode()


class MainPost(BaseModel):
    user_id: str
    test_message: str
    key: str



