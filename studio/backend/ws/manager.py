import json
import asyncio
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
import redis.asyncio as aioredis

router = APIRouter()
CHANNEL = "studio:events"


class WebSocketManager:
    def __init__(self):
        self.connections: list[WebSocket] = []
        self.redis: aioredis.Redis | None = None
        self.router = APIRouter()
        self.router.add_api_websocket_route("/ws", self.endpoint)

    async def connect_redis(self, redis: aioredis.Redis):
        self.redis = redis
        asyncio.create_task(self._listen())

    async def _listen(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(CHANNEL)
        async for message in pubsub.listen():
            if message["type"] == "message":
                await self._broadcast(message["data"].decode())

    async def publish(self, event_type: str, data: Any):
        payload = json.dumps({"type": event_type, "data": data})
        if self.redis:
            await self.redis.publish(CHANNEL, payload)

    async def _broadcast(self, message: str):
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections.remove(ws)

    async def endpoint(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self.connections.remove(websocket)


ws_manager = WebSocketManager()
