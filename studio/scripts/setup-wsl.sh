#!/bin/bash
# WSL2 Ubuntu 24.04 kurulum scripti

set -e
echo "=== Studio WSL2 Kurulumu ==="

# Sistem güncellemesi
sudo apt-get update && sudo apt-get upgrade -y

# Python 3.12
sudo apt-get install -y python3.12 python3.12-venv python3-pip

# Redis
sudo apt-get install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Git + DVC
sudo apt-get install -y git
pip install dvc

# Python bağımlılıkları
cd ~/studio/backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Conda (LingBot-Map için)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p ~/miniconda
rm miniconda.sh
~/miniconda/bin/conda init bash
source ~/.bashrc

# LingBot-Map
conda create -n lingbot python=3.10 -y
conda run -n lingbot pip install torch==2.8.0 torchvision --index-url https://download.pytorch.org/whl/cu128
git clone https://github.com/Robbyant/lingbot-map.git ~/lingbot-map
cd ~/lingbot-map
conda run -n lingbot pip install -e .
conda run -n lingbot python -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='robbyant/lingbot-map', local_dir='./checkpoints')
"

echo "=== WSL2 Kurulumu Tamamlandı ==="
