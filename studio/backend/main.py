from contextlib import asynccontextmanager
import aiosqlite
import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import projects, blender, ai, recon, export
from ws.manager import ws_manager
from models.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await aioredis.from_url(settings.redis_url)
    app.state.db = await aiosqlite.connect("studio.db")
    await init_db(app.state.db)
    await ws_manager.connect_redis(app.state.redis)
    yield
    await app.state.redis.aclose()
    await app.state.db.close()


app = FastAPI(title="Studio API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(blender.router, prefix="/api/blender", tags=["blender"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(recon.router, prefix="/api/recon", tags=["recon"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(ws_manager.router, tags=["ws"])


@app.get("/health")
async def health():
    return {"status": "ok"}
