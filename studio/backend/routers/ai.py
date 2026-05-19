import uuid
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services import ollama_service

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str
    model: str | None = None


class PullRequest(BaseModel):
    name: str


@router.get("/models")
async def list_models():
    return await ollama_service.list_models()


@router.post("/models/pull")
async def pull_model(req: PullRequest):
    async def stream():
        async for line in ollama_service.pull_model(req.name):
            yield line + "\n"
    return StreamingResponse(stream(), media_type="text/plain")


@router.post("/chat")
async def chat(req: ChatRequest):
    messages = [{"role": "user", "content": req.message}]

    async def stream():
        async for token in ollama_service.chat_stream(messages, req.model):
            yield token

    return StreamingResponse(stream(), media_type="text/plain")
