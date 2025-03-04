from starlette.websockets import WebSocket

import asyncio
from aio_pika import connect, Message, IncomingMessage, ExchangeType


class Notifier:
    def __init__(self, host: str, username: str, password: str, exchange_name: str):
        self._host = host
        self._username = username
        self._password = password
        self._connections: list[WebSocket] = []
        self._is_ready = False
        self._rabbitmq_connection = None
        self._exchange_name = exchange_name
        self._channel = None
        self._exchange = None
        self._queue_name = None

    async def subscribe(self):
        self._rabbitmq_connection = conn = await connect(
            host=self._host,
            login=self._username,
            password=self._password,
            loop=asyncio.get_running_loop(),
        )
        self._channel = channel = await conn.channel()
        self._exchange = await channel.declare_exchange(
            self._exchange_name, ExchangeType.FANOUT
        )
        queue = await channel.declare_queue(auto_delete=True)
        await queue.bind(self._exchange_name)
        self._queue_name = queue.name
        await queue.consume(self._notify, no_ack=True)
        self._is_ready = True

    async def unsubscribe(self):
        await self._channel.close()
        await self._rabbitmq_connection.close()

    async def publish(self, msg: str):
        await self._exchange.publish(
            Message(msg.encode("utf8"), content_encoding="utf8"),
            routing_key=self._queue_name,
        )

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self._connections.remove(websocket)

    async def _notify(self, message: IncomingMessage):
        updated_connections = []
        while len(self._connections) > 0:
            websocket = self._connections.pop()
            await websocket.send_text(message.body.decode("utf8"))
            updated_connections.append(websocket)
        self._connections = updated_connections

    @property
    def is_ready(self):
        return self._is_ready
