#!/bin/bash
# LingBot-Map Kurulum Scripti
# Robbyant (Ant Group) - Açık Kaynak 3D Yeniden Yapılandırma Modeli
# Gereksinim: CUDA 12.8 destekli GPU, 6GB+ VRAM önerilir

set -e

echo "=== LingBot-Map Kurulumu Başlıyor ==="

# 1. Conda ortamı oluştur
conda create -n lingbot python=3.10 -y
conda activate lingbot

# 2. PyTorch 2.8.0 + CUDA 12.8 kur
pip install torch==2.8.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 3. Repoyu klonla
git clone https://github.com/Robbyant/lingbot-map.git
cd lingbot-map

# 4. Bağımlılıkları kur
pip install -e .

# 5. (Opsiyonel) FlashInfer - hızlı streaming için
pip install flashinfer -f https://flashinfer.ai/whl/cu128/torch2.8/

# 6. Model ağırlıklarını indir (Hugging Face)
pip install huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='robbyant/lingbot-map', local_dir='./checkpoints')
"

echo "=== Kurulum Tamamlandı ==="
echo "Kullanım için: scripts/calistir.sh"
