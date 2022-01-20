from pydantic import BaseModel
from typing import Optional


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

