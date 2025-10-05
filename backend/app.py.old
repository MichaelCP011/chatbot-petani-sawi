# =============================================================================
# Import Library
# =============================================================================
import os
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
import numpy as np
from waitress import serve

# =============================================================================
# Inisialisasi Aplikasi Flask & Model AI
# =============================================================================
# Mendefinisikan lokasi folder 'static' dan 'templates'
app = Flask(__name__, static_folder='static', template_folder='templates')

# Konfigurasi CORS untuk keamanan
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Memuat Model AI ---
MODEL_PATH = 'chili_disease_model_final.keras'
print(f"[*] Memuat model dari {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"[*] Model berhasil dimuat.")

# --- Definisikan Nama Kelas (Urutan harus sama persis dengan saat training) ---
CLASS_NAMES = ['healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish']

# --- Basis Pengetahuan (Knowledge Base) ---
knowledge_base = {
    "leaf spot": {
        "description": "Bercak Daun (Cercospora) adalah penyakit jamur yang menyebabkan bercak pada daun, mengurangi kemampuan fotosintesis tanaman.",
        "handling": "1. Sanitasi: Buang dan bakar daun yang terinfeksi parah.\n2. Fungisida: Semprot dengan fungisida berbahan aktif Mankozeb atau Klorotalonil sesuai dosis anjuran.",
        "prevention": "1. Jaga Jarak Tanam: Pastikan sirkulasi udara baik.\n2. Rotasi Tanaman: Hindari menanam sawi di lahan yang sama secara terus-menerus."
    },
    "leaf curl": {
        "description": "Keriting Daun disebabkan oleh virus Gemini yang ditularkan oleh hama kutu kebul (whitefly). Penyakit ini membuat daun mengeriting dan pertumbuhan tanaman terhambat.",
        "handling": "1. Cabut dan musnahkan tanaman yang terinfeksi untuk mencegah penyebaran.\n2. Kendalikan hama vektor (kutu kebul) dengan insektisida sistemik.",
        "prevention": "1. Gunakan benih yang tahan atau toleran terhadap virus.\n2. Pasang perangkap likat kuning untuk memantau dan mengurangi populasi kutu kebul."
    },
    "whitefly": {
        "description": "Kutu Kebul (Whitefly) adalah hama penghisap getah tanaman. Selain merusak tanaman secara langsung, hama ini juga merupakan vektor utama penyebaran virus keriting daun (leaf curl).",
        "handling": "Semprot dengan insektisida berbahan aktif imidakloprid, tiametoksam, atau abamektin. Lakukan penyemprotan pada sore hari.",
        "prevention": "Gunakan mulsa plastik perak untuk mengusir hama. Tanam tanaman refugia seperti bunga tahi ayam (tagetes) di sekitar lahan."
    },
    "yellowish": {
        "description": "Daun Menguning (Yellowish) atau klorosis bisa disebabkan oleh beberapa faktor, seperti kekurangan unsur hara (terutama Nitrogen) atau gejala awal serangan virus.",
        "handling": "Jika karena nutrisi, berikan pupuk nitrogen (Urea) atau pupuk daun yang seimbang. Jika gejala disertai keriting, kemungkinan besar karena virus dan tanaman harus dimusnahkan.",
        "prevention": "Pastikan pemupukan dilakukan secara teratur dan berimbang sesuai kebutuhan tanaman. Jaga kebersihan kebun untuk mengendalikan hama penyebar virus."
    },
    "healthy": {
        "description": "Tanaman Anda dalam kondisi sehat dan tidak menunjukkan gejala serangan hama atau penyakit.",
        "handling": "Tidak ada tindakan penanganan yang diperlukan. Pertahankan kondisi ini.",
        "prevention": "Terus lakukan praktik budidaya yang baik seperti penyiraman yang cukup, pemupukan berimbang, dan pemantauan rutin terhadap hama dan penyakit."
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
    
    return predicted_class, float(confidence)


# =============================================================================
# Definisi Rute (Endpoints)
# =============================================================================

# --- Rute untuk menyajikan halaman frontend ---
@app.route("/")
def home():
    """Menyajikan halaman utama chatbot (index.html)."""
    return render_template('index.html')

# --- Rute API untuk diagnosis gambar ---
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

# --- Rute API untuk detail informasi ---
@app.route("/api/details")
def get_details():
    disease_name = request.args.get('disease_name')
    info_type = request.args.get('info_type')
    
    disease_data = knowledge_base.get(disease_name, {})
    detail_info = disease_data.get(info_type)
    
    if not detail_info:
        return jsonify({"status": "error", "message": "Informasi tidak ditemukan"}), 404
        
    return jsonify({"status": "success", "data": {"text": detail_info}})


# =============================================================================
# Menjalankan Aplikasi dengan Waitress
# =============================================================================
if __name__ == "__main__":
    print("[*] Menjalankan server di http://localhost:5000")
    serve(app, host="0.0.0.0", port=5000)