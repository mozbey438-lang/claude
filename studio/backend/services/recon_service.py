import asyncio
import uuid
from pathlib import Path
from config import settings
from ws.manager import ws_manager

GPU_LOCK = asyncio.Semaphore(1)


async def start_reconstruction(video_path: str, output_dir: str) -> str:
    job_id = str(uuid.uuid4())
    asyncio.create_task(_run(job_id, video_path, output_dir))
    return job_id


async def _run(job_id: str, video_path: str, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        settings.lingbot_map_path,
        "--video", video_path,
        "--output", output_dir,
        "--mask_sky",
        "--offload_to_cpu",
    ]

    async with GPU_LOCK:
        await ws_manager.publish("job.progress", {"job_id": job_id, "percent": 0, "message": "Başlıyor..."})

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        async for line in proc.stdout:
            text = line.decode().strip()
            percent = _parse_percent(text)
            await ws_manager.publish("job.progress", {"job_id": job_id, "percent": percent, "message": text})

        await proc.wait()
        success = proc.returncode == 0
        await ws_manager.publish(
            "job.done" if success else "job.error",
            {"job_id": job_id, "output_dir": output_dir}
        )


def _parse_percent(line: str) -> int:
    import re
    m = re.search(r"(\d+)%", line)
    return int(m.group(1)) if m else 0
