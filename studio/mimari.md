# Studio — Sistem Mimarisi

## Genel Bakış

```
┌──────────────────────────────────────────────────────────────┐
│               ELECTRON SHELL (Host Süreci)                   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │         REACT FRONTEND  (localhost:5173)               │   │
│  │  ┌─────────┐ ┌─────────┐ ┌──────┐ ┌───────────────┐  │   │
│  │  │ Projeler│ │ Blender │ │  AI  │ │    Export     │  │   │
│  │  └────┬────┘ └────┬────┘ └──┬───┘ └───────┬───────┘  │   │
│  │       └───────────┴─────────┴─────────────┘           │   │
│  │                  REST + WebSocket                      │   │
│  └──────────────────────┬────────────────────────────────┘   │
└─────────────────────────┼────────────────────────────────────┘
                          │
           ┌──────────────▼──────────────┐
           │   FASTAPI BACKEND (WSL2)    │
           │   localhost:8000            │
           │                             │
           │  /api/projects  (git)       │
           │  /api/blender   (MCP)       │
           │  /api/ai        (Ollama)    │
           │  /api/recon     (LingBot)   │
           │  /api/export    (motorlar)  │
           │  /ws            (olaylar)   │
           └──────┬──────────────────────┘
                  │
     ┌────────────┼──────────────────────────────┐
     │            │            │                  │
┌────▼───┐  ┌─────▼──┐  ┌─────▼────┐  ┌─────────▼──────┐
│ GitPy  │  │Blender │  │  Ollama  │  │  LingBot-Map   │
│  DVC   │  │  MCP   │  │ :11434   │  │  (subprocess)  │
└────┬───┘  └────────┘  └──────────┘  └────────────────┘
     │
┌────▼────────────────────────────┐
│    GIT REPO (proje deposu)      │
│  /projects/<isim>/              │
│    assets/ exports/ ai-logs/    │
└────┬────────────────────────────┘
     │ Tailscale tüneli
┌────▼────────────────┐
│   MOBİL TARAYICI   │
│   (PWA, aynı UI)   │
└─────────────────────┘
```

## Katmanlar

| Katman | Teknoloji | Görev |
|---|---|---|
| Masaüstü kabuğu | Electron 32 | .exe paketi, backend yönetimi |
| Arayüz | React 18 + Vite + Zustand | Kullanıcı panelleri |
| Backend | FastAPI + Uvicorn (WSL2) | Tüm bileşenleri koordine eder |
| 3D | Blender 4.2 LTS + MCP addon | Modelleme ve render |
| Yerel AI | Ollama + Llama 3.2 3B | Asistan, komut üretimi |
| 3D Tarama | LingBot-Map | Video → Point cloud → Mesh |
| Versiyon | Git + DVC | Proje ve büyük dosya yönetimi |
| Uzaktan | Tailscale + JWT + PWA | Mobil kontrol |

## Yapı Aşamaları

| Aşama | Hedef | Durum |
|---|---|---|
| 1 | Electron + Backend + Git projeler | Hazır (iskelet) |
| 2 | AI konsol (Ollama streaming) | Hazır (iskelet) |
| 3 | Blender MCP entegrasyonu | Hazır (iskelet) |
| 4 | Tailscale uzaktan erişim | Hazır (iskelet) |
| 5 | LingBot-Map 3D tarama | Disk bekleniyor |
| 6 | Oyun motoru export | Disk bekleniyor |

## GPU Kısıtı (GTX 1650 Ti 4GB)

```python
# recon_service.py
GPU_LOCK = asyncio.Semaphore(1)  # Aynı anda tek GPU işi
```

LingBot-Map ve Ollama aynı anda çalışmaz. GPU güncellemesinde bu limit kaldırılır.
