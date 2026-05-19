import asyncio
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import settings
import json
from pathlib import Path

router = APIRouter()

_jobs: dict[str, dict] = {}


class ExportRequest(BaseModel):
    project_id: str
    blend_file: str
    output_path: str


@router.post("/{engine}")
async def export(engine: str, req: ExportRequest):
    if engine not in ("godot", "unreal", "unity"):
        raise HTTPException(400, "Desteklenmeyen motor")

    engines_cfg = json.loads(Path("config/engines.json").read_text())
    if engine not in engines_cfg:
        raise HTTPException(500, f"{engine} yapılandırılmamış")

    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "running", "engine": engine}
    asyncio.create_task(_run_export(job_id, engine, engines_cfg[engine], req))
    return {"job_id": job_id}


async def _run_export(job_id: str, engine: str, engine_cfg: dict, req: ExportRequest):
    executable = engine_cfg["executable"]
    try:
        if engine == "godot":
            cmd = [executable, "--export-release", "Linux/X11", req.output_path]
        elif engine == "unreal":
            cmd = [executable, req.blend_file, "-run=Python", f"import unreal; unreal.export('{req.output_path}')"]
        elif engine == "unity":
            cmd = [executable, "-batchmode", "-quit", "-projectPath", req.output_path]

        proc = await asyncio.create_subprocess_exec(*cmd)
        await proc.wait()
        _jobs[job_id]["status"] = "done" if proc.returncode == 0 else "error"
    except Exception as e:
        _jobs[job_id] = {"status": "error", "error": str(e)}


@router.get("/jobs/{job_id}")
async def job_status(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(404, "İş bulunamadı")
    return _jobs[job_id]
