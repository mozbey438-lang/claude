import asyncio
import json
from config import settings

_id_counter = 0


def _next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


class BlenderService:
    def __init__(self):
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._pending: dict[int, asyncio.Future] = {}
        self._lock = asyncio.Lock()

    async def _ensure_connected(self):
        if self._writer and not self._writer.is_closing():
            return
        host = settings.resolve_windows_host_ip()
        self._reader, self._writer = await asyncio.open_connection(host, settings.blender_mcp_port)
        asyncio.create_task(self._receive_loop())

    async def _receive_loop(self):
        while True:
            try:
                line = await self._reader.readline()
                if not line:
                    break
                data = json.loads(line)
                fut = self._pending.pop(data.get("id"), None)
                if fut and not fut.done():
                    if "error" in data:
                        fut.set_exception(RuntimeError(data["error"]["message"]))
                    else:
                        fut.set_result(data.get("result"))
            except Exception:
                break

    async def execute(self, method: str, params: dict | None = None) -> any:
        async with self._lock:
            await self._ensure_connected()
        call_id = _next_id()
        payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}, "id": call_id})
        loop = asyncio.get_event_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending[call_id] = fut
        self._writer.write((payload + "\n").encode())
        await self._writer.drain()
        return await asyncio.wait_for(fut, timeout=30.0)

    async def run_python(self, code: str) -> any:
        return await self.execute("execute_python", {"code": code})

    async def is_alive(self) -> bool:
        try:
            await self.execute("ping")
            return True
        except Exception:
            return False


blender = BlenderService()
