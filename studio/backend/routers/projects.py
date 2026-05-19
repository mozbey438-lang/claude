from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import git_service

router = APIRouter()


class CreateProjectRequest(BaseModel):
    name: str


class CommitRequest(BaseModel):
    message: str
    files: list[str] | None = None


@router.get("")
async def list_projects():
    return git_service.list_projects()


@router.post("")
async def create_project(req: CreateProjectRequest):
    return git_service.create_project(req.name)


@router.get("/{project_id}")
async def get_project(project_id: str):
    projects = git_service.list_projects()
    p = next((p for p in projects if p["id"] == project_id), None)
    if not p:
        raise HTTPException(404, "Proje bulunamadı")
    return p


@router.post("/{project_id}/commit")
async def commit(project_id: str, req: CommitRequest):
    sha = git_service.commit(project_id, req.message, req.files)
    return {"sha": sha}


@router.get("/{project_id}/history")
async def history(project_id: str, limit: int = 20):
    return git_service.get_history(project_id, limit)
