import httpx
from typing import AsyncIterator
from config import settings


async def list_models() -> list[str]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.ollama_base_url}/api/tags")
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]


async def pull_model(name: str) -> AsyncIterator[str]:
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", f"{settings.ollama_base_url}/api/pull", json={"name": name}) as r:
            async for line in r.aiter_lines():
                if line:
                    yield line


async def chat_stream(
    messages: list[dict],
    model: str | None = None,
) -> AsyncIterator[str]:
    model = model or settings.ollama_default_model
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            f"{settings.ollama_base_url}/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        ) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done"):
                        break
