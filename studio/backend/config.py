import subprocess
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    redis_url: str = "redis://localhost:6379"

    projects_root: str = "/home/user/studio/projects"
    dvc_remote: str = "local"

    blender_executable: str = "blender"
    blender_mcp_port: int = 6789
    windows_host_ip: str = "auto"

    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "llama3.2:3b"

    lingbot_map_path: str = "/usr/local/bin/lingbot-map"

    jwt_secret: str = "changeme"
    jwt_expire_hours: int = 72

    tailscale_ip: str = "auto"

    def resolve_windows_host_ip(self) -> str:
        if self.windows_host_ip != "auto":
            return self.windows_host_ip
        try:
            result = subprocess.run(
                ["grep", "nameserver", "/etc/resolv.conf"],
                capture_output=True, text=True
            )
            return result.stdout.split()[1]
        except Exception:
            return "host.docker.internal"

    def resolve_tailscale_ip(self) -> str:
        if self.tailscale_ip != "auto":
            return self.tailscale_ip
        try:
            result = subprocess.run(["tailscale", "ip"], capture_output=True, text=True)
            return result.stdout.strip().split("\n")[0]
        except Exception:
            return ""


settings = Settings()
