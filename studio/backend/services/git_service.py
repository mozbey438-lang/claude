import os
from pathlib import Path
import git
from config import settings


def _repo_path(project_id: str) -> Path:
    return Path(settings.projects_root) / project_id


def list_projects() -> list[dict]:
    root = Path(settings.projects_root)
    root.mkdir(parents=True, exist_ok=True)
    projects = []
    for p in root.iterdir():
        if p.is_dir() and (p / ".git").exists():
            repo = git.Repo(p)
            projects.append({
                "id": p.name,
                "name": p.name,
                "last_commit": repo.head.commit.message.strip() if repo.head.is_valid() else None,
                "branch": repo.active_branch.name,
            })
    return projects


def create_project(name: str) -> dict:
    path = _repo_path(name)
    path.mkdir(parents=True, exist_ok=True)
    repo = git.Repo.init(path)
    (path / ".gitkeep").touch()
    repo.index.add([".gitkeep"])
    repo.index.commit(f"Proje oluşturuldu: {name}")
    return {"id": name, "name": name, "path": str(path)}


def commit(project_id: str, message: str, files: list[str] | None = None) -> str:
    path = _repo_path(project_id)
    repo = git.Repo(path)
    if files:
        repo.index.add(files)
    else:
        repo.git.add(A=True)
    commit = repo.index.commit(message)
    return commit.hexsha


def get_history(project_id: str, limit: int = 20) -> list[dict]:
    path = _repo_path(project_id)
    repo = git.Repo(path)
    return [
        {
            "sha": c.hexsha[:8],
            "message": c.message.strip(),
            "author": c.author.name,
            "date": c.committed_datetime.isoformat(),
        }
        for c in repo.iter_commits(max_count=limit)
    ]
