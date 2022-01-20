import uvicorn
from fastapi import FastAPI, WebSocket
from Server.Config.config import config_args
from Server.Get.get_class import DefaultMessage

app = FastAPI()


@app.get('/')
async def main(default: DefaultMessage) -> str:
    return DefaultMessage.send_message()


@app.websocket('/socket')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message : {data}")


if __name__ == '__main__':
    uvicorn.run(app, host=config_args.SERVER_URL_ADDRESS, port=config_args.SERVER_PORT_NUMBER)
