from os import environ

import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket, WebSocketDisconnect

from .notifier import Notifier


app = FastAPI()
notifier = Notifier(
    environ.get("NOTIFIER_RABBITMQ_HOST"),
    environ.get("NOTIFIER_RABBITMQ_USER"),
    environ.get("NOTIFIER_RABBITMQ_PASSWORD"),
    environ.get("NOTIFIER_EXCHANGE", "chat"),
)
with open("assets/index.html", "r") as f:
    INDEX_HTML = f.read()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if not notifier.is_ready:
        await notifier.subscribe()
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await notifier.publish(data)
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/")
async def get():
    return HTMLResponse(INDEX_HTML)


if __name__ == "__main__":
    uvicorn.run(
        app,
    )
