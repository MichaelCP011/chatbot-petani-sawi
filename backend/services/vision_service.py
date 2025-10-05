# backend/services/vision_service.py
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# --- Konfigurasi Model CV ---
MODEL_PATH = 'chili_disease_model_final.keras'
CLASS_NAMES = ['healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish']
IMAGE_SIZE = (224, 224)

# --- Memuat Model (hanya sekali saat server dimulai) ---
print(f"[*] Memuat model CV dari {MODEL_PATH}...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("[*] Model CV berhasil dimuat.")
except Exception as e:
    print(f"[ERROR] Gagal memuat model CV: {e}")
    model = None

# --- Fungsi Prediksi ---
def predict_image_from_file(file_storage):
    """Menerima file gambar, memproses, dan mengembalikan prediksi."""
    if not model:
        raise RuntimeError("Model CV tidak berhasil dimuat.")

    temp_path = "temp_image_for_prediction.jpg"
    file_storage.save(temp_path)

    img = image.load_img(temp_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_batch)
    
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = np.max(predictions[0]) * 100

    os.remove(temp_path)
    
    return predicted_class, float(confidence)