from abc import ABCMeta, abstractmethod
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from fastapi.responses import JSONResponse
from Server.Middleware.ban_list import BanList, ban_list


class IPConnector(metaclass=ABCMeta):
    @abstractmethod
    async def self_check(self):
        pass

    @abstractmethod
    async def outer_check(self, target_list: list):
        pass


class IPChecker(BanList, IPConnector):
    def __init__(self, ip: str):
        self.__target_ip: str = ip
        BanList.__init__(self)

    async def self_check(self) -> bool:
        if self.__target_ip in self.target_ban_list:
            return True
        else:
            return False

    async def outer_check(self, target_list: list) -> bool:
        if self.__target_ip in target_list:
            return True
        else:
            return False


class TargetBenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        ip_checker = IPChecker(request.client.host)
        if await ip_checker.outer_check(ban_list.target_ban_list) is True:
            #  정확한 에러 상태를 보낼 수 있는 방법에 대해 더 알아볼 것
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Allowed"})
        else:
            pass_request = await call_next(request)
            return pass_request