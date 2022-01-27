from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context
from Server.Middleware.ban_list import BanList, ban_list


class LoginUserName(BanList):

    @classmethod
    async def take_login_name(cls, request: Request, call_next):
        context.update(is_pass=True)
        response = await call_next(request)
        if context["user_id"] in ban_list.target_ban_list:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not Allowed"})
        # 특정 행동 이후 Ban 목록에 넣으려면 Middleware에서 처리해야 함
        await ban_list.add_ban(context["user_id"])
        return response
