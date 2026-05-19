from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import recon_service

router = APIRouter()

_jobs: dict[str, str] = {}


class ReconRequest(BaseModel):
    video_path: str
    output_dir: str


@router.post("/start")
async def start(req: ReconRequest):
    job_id = await recon_service.start_reconstruction(req.video_path, req.output_dir)
    _jobs[job_id] = "running"
    return {"job_id": job_id}


@router.get("/jobs/{job_id}")
async def job_status(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(404, "İş bulunamadı")
    return {"job_id": job_id, "status": _jobs[job_id]}
