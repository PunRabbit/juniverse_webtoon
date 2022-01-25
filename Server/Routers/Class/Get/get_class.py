from fastapi.params import Query
from pydantic import BaseModel
from typing import Optional
from bcrypt import hashpw, gensalt


class DefaultMessage(BaseModel):
    message: str = 'Hello'
    initial_ip: Optional[str]

    @classmethod
    def send_message(cls, user_ip: int = None) -> str:
        if cls.initial_ip is False and user_ip is None:
            target_message: str = cls.message + cls.initial_ip
        else:
            target_message: str = cls.message + str(user_ip)
        return target_message


class MainItem(BaseModel):
    message: str = "Hi"
    ban_user: Optional[str] = Query("None", description="Default value is None")


class HistoryGet(BaseModel):
    fields: list
    brand: list = Query(None, description="brand name")


class LoginGet(BaseModel):
    user_id: str
    password: str

    async def bcrypt(self):
        byte_password: bytes = self.password.encode('UTF-8')
        bcrypt_password: str = hashpw(byte_password, gensalt(12)).decode('UTF-8')


class MainGet(BaseModel):
    user_id: str
    test_message: str