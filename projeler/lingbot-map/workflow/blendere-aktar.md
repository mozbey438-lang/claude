# LingBot-Map → Blender İş Akışı

## Adımlar

### 1. Video Çek
- Telefon ile mekan videola (MP4, 1080p yeterli)
- Yavaş ve sabit hareket et, titreme olmasın
- İyi aydınlatma kritik

### 2. LingBot-Map ile İşle
```bash
./scripts/calistir.sh video.mp4
```
Çıktı: `cikti/TARIH/` klasöründe NPZ point cloud dosyaları

### 3. Point Cloud → OBJ Dönüşümü
```python
# point_cloud_to_obj.py
import numpy as np
import open3d as o3d

# NPZ dosyasını yükle
data = np.load("cikti/tahmin.npz")
points = data["points"]

# Open3D ile OBJ'ye dönüştür
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Mesh oluştur (Poisson yüzey yeniden yapılandırma)
mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
o3d.io.write_triangle_mesh("model.obj", mesh)
```

### 4. Blender'a Aktar
- File → Import → Wavefront (.obj)
- Ölçeği ayarla
- Gereksiz geometriyi temizle
- Texture/malzeme uygula (Blender MCP ile)

### 5. Oyun Motoruna Export
- File → Export → glTF 2.0
- Godot/Unity/UE5'e aktar

## Bursa Projesi İçin
Bu iş akışını kullanarak:
- Bursa sokaklarını videola
- Otomatik 3D modele dönüştür
- Blender'da düzenle
- Oyun motoruna aktar
