from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.blender_service import blender

router = APIRouter()


class CommandRequest(BaseModel):
    code: str


class OpenRequest(BaseModel):
    filepath: str


@router.get("/status")
async def status():
    alive = await blender.is_alive()
    return {"alive": alive}


@router.post("/command")
async def command(req: CommandRequest):
    try:
        result = await blender.run_python(req.code)
        return {"result": result}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/open")
async def open_file(req: OpenRequest):
    code = f"bpy.ops.wm.open_mainfile(filepath={req.filepath!r})"
    result = await blender.run_python(code)
    return {"result": result}


@router.post("/render")
async def render():
    code = "bpy.ops.render.render(write_still=True)"
    result = await blender.run_python(code)
    return {"result": result}
