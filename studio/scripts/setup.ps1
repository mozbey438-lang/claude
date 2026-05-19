# Windows kurulum scripti (PowerShell)
# Yonetici olarak calistir

Write-Host "=== Studio Windows Kurulumu ===" -ForegroundColor Cyan

# Winget kontrol
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "winget bulunamadi. Microsoft Store'dan App Installer yukle."
    exit 1
}

# Node.js 20 LTS
winget install OpenJS.NodeJS.LTS -e

# Blender 4.2 LTS
winget install BlenderFoundation.Blender -e

# Ollama
winget install Ollama.Ollama -e

# Tailscale
winget install tailscale.tailscale -e

# WSL2
wsl --install -d Ubuntu-24.04

# Blender MCP addon kur
$BlenderAddon = "studio/scripts/blender-addon/studio_mcp.py"
$BlenderScripts = "$env:APPDATA\Blender Foundation\Blender\4.2\scripts\addons"
New-Item -ItemType Directory -Force -Path $BlenderScripts
Copy-Item $BlenderAddon $BlenderScripts

# Ollama modeli indir
Start-Process ollama -ArgumentList "pull llama3.2:3b" -Wait

Write-Host "=== Kurulum Tamamlandi ===" -ForegroundColor Green
Write-Host "Sonraki adim: WSL2 icinde setup-wsl.sh calistir" -ForegroundColor Yellow
