# LingBot-Map Sistem Gereksinimleri

## Minimum
- GPU: 6GB VRAM, CUDA 7.5+
- RAM: 16GB
- Disk: 20GB boş alan (model + bağımlılıklar)
- Python: 3.10
- OS: Ubuntu 20.04+ / Windows 11 (WSL2 önerilir)

## Önerilen
- GPU: RTX 3060 12GB ve üzeri
- RAM: 32GB
- Disk: SSD 50GB+

## Mevcut Donanım Notu (i5-10. Nesil / GTX 1650 Ti 4GB)
- `--offload_to_cpu` flag ile çalışır ama yavaş
- Kısa videolar (max 60 sn) için uygun
- Hardware güncelleme sonrası tam performans alınır

## CUDA Versiyon Tablosu
| GPU Serisi | CUDA Desteği | LingBot-Map |
|---|---|---|
| GTX 1650 Ti (mevcut) | 7.5 | Yavaş (CPU offload) |
| RTX 3060 | 8.6 | İyi |
| RTX 3080/4080 | 8.6/8.9 | Tam performans |
