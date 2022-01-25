import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import Server.Routers.webtoon_page
from Server.Config.config import config_args
from Server.Routers.Class.Get.get_class import DefaultMessage
from Server.Middleware.ban_ip import TargetBenMiddleware
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from Server.Routers.Security.cryptography_module import CryptographyKeyGenerator
from Server.Routers.Class.Post.post_class import MainPost
from Server.Routers.Class.Get.get_class import MainGet



def create_app():
    new_app = FastAPI()
    new_app.middleware('http')()
    new_app.add_middleware(ContextMiddleware)
    new_app.add_middleware(TargetBenMiddleware)
    # cors 등록 (개발단계 전체 허용)
    new_app.add_middleware(CORSMiddleware,
                           allow_origins=['*'],
                           allow_credentials=True,
                           allow_methods=['*'],
                           allow_headers=['*'])
    new_app.mount("/", StaticFiles(directory="Static", html=True), name="static")

    return new_app


app = create_app()
app.include_router(Server.Routers.webtoon_page.router)


@app.get('/')
async def main(default: DefaultMessage) -> str:
    return DefaultMessage.send_message()


@app.get('/main')
async def main_page(response: MainGet):
    return "Hi! I'm Here!"


@app.post('/main')
async def test_main_page(response: MainPost):
    context.update(user_id=response.user_id)
    key_generator = CryptographyKeyGenerator(response.key)
    await key_generator.gen_key()
    return f"Hi! I'm Here! {response.test_message}"

@app.websocket('/socket')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message : {data}")


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=config_args.SERVER_URL_ADDRESS,
                port=config_args.SERVER_PORT_NUMBER)
