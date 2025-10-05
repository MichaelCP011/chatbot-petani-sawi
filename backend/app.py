from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Basis Pengetahuan (Knowledge Base) Sederhana ---
# Kita buat database tiruan di dalam kode untuk saat ini.
knowledge_base = {
    "Bercak Daun (Cercospora) - Hasil Simulasi": {
        "description": "Penyakit yang disebabkan oleh jamur Cercospora sp. yang menyebabkan bercak-bercak pada daun, mengurangi kemampuan fotosintesis tanaman.",
        "handling": "1. Sanitasi: Buang dan bakar daun yang terinfeksi parah.\n2. Fungisida: Semprot dengan fungisida berbahan aktif Mankozeb atau Klorotalonil sesuai dosis anjuran.",
        "prevention": "1. Jaga Jarak Tanam: Pastikan sirkulasi udara baik.\n2. Rotasi Tanaman: Hindari menanam sawi di lahan yang sama secara terus-menerus.\n3. Benih Sehat: Gunakan benih yang bebas dari patogen."
    }
    # Anda bisa menambahkan data penyakit lain di sini
}

# --- Endpoint untuk mengambil detail spesifik ---
@app.route("/api/details") # Metode default adalah GET
def get_details():
    # Ambil parameter dari URL, contoh: /api/details?disease_name=...&info_type=...
    disease_name = request.args.get('disease_name')
    info_type = request.args.get('info_type') # 'description', 'handling', atau 'prevention'

    # Cari data di knowledge base
    disease_data = knowledge_base.get(disease_name)

    if not disease_data:
        return jsonify({"status": "error", "message": "Penyakit tidak ditemukan"}), 404

    detail_info = disease_data.get(info_type)
    
    if not detail_info:
        return jsonify({"status": "error", "message": "Tipe informasi tidak valid"}), 404

    return jsonify({"status": "success", "data": {"text": detail_info}})


# --- Endpoint Utama untuk Diagnosis Awal ---
@app.route("/api/diagnose", methods=['POST'])
def diagnose():
    # 1. Periksa apakah ada file dalam request
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada file gambar yang dikirim"}), 400

    file = request.files['image']

    # 2. Periksa apakah nama filenya tidak kosong
    if file.filename == '':
        return jsonify({"status": "error", "message": "Tidak ada file yang dipilih"}), 400

    # 3. Jika file ada, cetak namanya ke terminal untuk konfirmasi
    if file:
        print(f"[*] Berhasil menerima file: {file.filename}")
        # Di langkah selanjutnya, file ini akan dikirim ke model CV
    
    # --- Respons simulasi tetap sama untuk saat ini ---
    disease_name = "Bercak Daun (Cercospora) - Hasil Simulasi"
    disease_info = knowledge_base.get(disease_name)

    mock_response = {
        "status": "success",
        "data": {
            "disease_name": disease_name,
            "confidence": 0.92,
            "description": disease_info.get("description"),
            "handling_options": [
                { "title": "Info Lengkap Penyakit", "action": "description" },
                { "title": "Cara Penanganan", "action": "handling" },
                { "title": "Cara Pencegahan", "action": "prevention" }
            ]
        }
    }
    return jsonify(mock_response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)