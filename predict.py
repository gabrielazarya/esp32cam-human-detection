import sys
import cv2
import pickle
import numpy as np

# Ambil path dari argumen atau default ke "input.jpg"
path = sys.argv[1] if len(sys.argv) > 1 else "upload/input.jpg"

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load label map
with open("label_map.pkl", "rb") as f:
    label_map = pickle.load(f)

# Baca gambar
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
if img is None:
    print(f"[ERROR] Gambar '{path}' tidak ditemukan atau tidak bisa dibuka.")
    exit()

img = cv2.resize(img, (64, 64)) / 255.0
img = img.flatten().reshape(1, -1)

# Prediksi
pred = model.predict(img)[0]
label = label_map[pred]

print(f"Prediksi: {label}")

# Simpan ke file (dibaca ESP32)
with open("hasil.txt", "w") as f:
    f.write(label)
