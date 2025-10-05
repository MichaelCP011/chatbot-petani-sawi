# =============================================================================
# Import Library
# =============================================================================
import os
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
import numpy as np

# =============================================================================
# Inisialisasi Aplikasi Flask & Model AI
# =============================================================================
app = Flask(__name__)
CORS(app)

# --- Memuat Model AI ---
MODEL_PATH = 'chili_disease_model_final.keras'
print(f"[*] Memuat model dari {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"[*] Model berhasil dimuat.")

# --- Definisikan Nama Kelas ---
CLASS_NAMES = ['healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish']

# --- Basis Pengetahuan (Knowledge Base) ---
knowledge_base = {
    "leaf spot": {
        "description": "Bercak Daun (Cercospora) adalah penyakit jamur yang menyebabkan bercak pada daun, mengurangi fotosintesis.",
        "handling": "1. Sanitasi: Buang dan bakar daun terinfeksi.\n2. Fungisida: Semprot dengan fungisida berbahan aktif Mankozeb.",
        "prevention": "1. Jaga Jarak Tanam.\n2. Rotasi Tanaman."
    },
    "leaf curl": {
        "description": "Keriting Daun disebabkan oleh virus Gemini yang ditularkan oleh hama kutu kebul (whitefly).",
        "handling": "1. Cabut dan musnahkan tanaman terinfeksi.\n2. Kendalikan hama vektor dengan insektisida.",
        "prevention": "1. Gunakan benih tahan virus.\n2. Pasang perangkap serangga."
    },
    "whitefly": {
        "description": "Kutu Kebul (Whitefly) adalah hama penghisap getah yang bisa menularkan virus keriting daun.",
        "handling": "Semprot dengan insektisida berbahan aktif imidakloprid atau tiametoksam.",
        "prevention": "Gunakan mulsa plastik perak dan tanam tanaman refugia (penarik serangga)."
    },
    "yellowish": {
        "description": "Menguning (Yellowish) bisa disebabkan oleh kekurangan nutrisi (klorosis) atau serangan virus.",
        "handling": "Berikan pupuk nitrogen (urea) atau pupuk daun. Jika karena virus, musnahkan tanaman.",
        "prevention": "Pastikan pemupukan berimbang dan kendalikan hama penyebar virus."
    },
    "healthy": {
        "description": "Tanaman Anda terlihat sehat dan tidak menunjukkan gejala penyakit.",
        "handling": "Tidak ada tindakan penanganan yang diperlukan.",
        "prevention": "Terus lakukan praktik budidaya yang baik (penyiraman, pemupukan)."
    }
}


# =============================================================================
# Fungsi Helper untuk Prediksi
# =============================================================================
def predict_image(file_storage):
    temp_path = "temp_image.jpg"
    file_storage.save(temp_path)

    img = image.load_img(temp_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_batch)
    
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = np.max(predictions[0]) * 100

    os.remove(temp_path)
    
    # --- PERUBAHAN ADA DI SINI ---
    # "Terjemahkan" dari numpy.float32 menjadi float standar Python
    return predicted_class, float(confidence)


# =============================================================================
# Definisi Rute API (Endpoints)
# =============================================================================
@app.route("/api/diagnose", methods=['POST'])
def diagnose():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada file gambar"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Tidak ada file dipilih"}), 400

    try:
        predicted_class, confidence = predict_image(file)
        disease_info = knowledge_base.get(predicted_class, {})

        response_data = {
            "status": "success",
            "data": {
                "disease_name": predicted_class,
                "confidence": confidence,
                "description": disease_info.get("description", "Informasi tidak tersedia."),
                "handling_options": [
                    {"title": "Info Penyakit", "action": "description"},
                    {"title": "Cara Penanganan", "action": "handling"},
                    {"title": "Cara Pencegahan", "action": "prevention"}
                ]
            }
        }
        return jsonify(response_data)

    except Exception as e:
        print(f"[Error] {e}")
        return jsonify({"status": "error", "message": "Gagal memproses gambar."}), 500


@app.route("/api/details")
def get_details():
    disease_name = request.args.get('disease_name')
    info_type = request.args.get('info_type')
    
    disease_data = knowledge_base.get(disease_name)
    if not disease_data:
        return jsonify({"status": "error", "message": "Penyakit tidak ditemukan"}), 404

    detail_info = disease_data.get(info_type)
    if not detail_info:
        return jsonify({"status": "error", "message": "Tipe informasi tidak valid"}), 404
        
    return jsonify({"status": "success", "data": {"text": detail_info}})


# =============================================================================
# Menjalankan Aplikasi
# =============================================================================
if __name__ == "__main__":
    app.run(debug=False, port=5000)