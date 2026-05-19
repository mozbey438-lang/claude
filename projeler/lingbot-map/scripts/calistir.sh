#!/bin/bash
# LingBot-Map Çalıştırma Scripti
# Kullanım: ./calistir.sh <video_dosyasi.mp4>

set -e

VIDEO=$1
CIKTI_DIZIN="./cikti/$(date +%Y%m%d_%H%M%S)"
MODEL_PATH="./checkpoints/checkpoint.pt"

if [ -z "$VIDEO" ]; then
    echo "Kullanim: ./calistir.sh <video.mp4>"
    exit 1
fi

mkdir -p "$CIKTI_DIZIN"

conda activate lingbot

echo "=== 3D Yeniden Yapılandırma Başlıyor ==="
echo "Girdi: $VIDEO"
echo "Çıktı: $CIKTI_DIZIN"

# Standart mod (6GB+ VRAM)
# python demo.py --model_path $MODEL_PATH --video $VIDEO --output $CIKTI_DIZIN --mask_sky

# Düşük VRAM modu (GTX 1650 Ti için)
python demo.py \
    --model_path $MODEL_PATH \
    --video $VIDEO \
    --output $CIKTI_DIZIN \
    --mask_sky \
    --offload_to_cpu

echo "=== Tamamlandı: $CIKTI_DIZIN ==="
