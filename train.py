import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle

# === SETUP ===
dataset_dir = "dataset"
classes = ["manusia", "bukan_manusia"]
data = []
labels = []
label_map = {0: "manusia", 1: "bukan_manusia"}

print("[INFO] Memuat dataset...")

# === LOAD DATA ===
for label, folder in enumerate(classes):
    folder_path = os.path.join(dataset_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (64, 64)).astype(np.float32) / 255.0
            data.append(img.flatten())
            labels.append(label)
        except Exception as e:
            print(f"[WARNING] Gagal memuat {file_path}: {e}")

X = np.array(data)
y = np.array(labels)

print(f"[INFO] Data siap. Total sample: {len(X)}")

# === SPLIT DATA ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# === TRAIN MODEL ===
print("[INFO] Melatih model Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === EVALUASI ===
acc = model.score(X_test, y_test)
y_pred = model.predict(X_test)

print(f"[INFO] Akurasi: {acc:.2f}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=classes))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# === SAVE MODEL ===
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_map.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("[INFO] Model dan label_map berhasil disimpan!")
