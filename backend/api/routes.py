# backend/api/routes.py
from flask import Blueprint, request, jsonify, render_template
from services.vision_service import predict_image_from_file
from services.chatbot_service import get_chatbot_response

# Membuat Blueprint untuk API
api_blueprint = Blueprint('api', __name__, template_folder='../templates', static_folder='../static')

# Rute untuk menyajikan halaman frontend
@api_blueprint.route("/")
def home():
    return render_template('index.html')

# Rute untuk diagnosis gambar
@api_blueprint.route("/api/diagnose", methods=['POST'])
def diagnose():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada file gambar"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Tidak ada file dipilih"}), 400

    try:
        # 1. Dapatkan prediksi dari model CV
        predicted_class, confidence = predict_image_from_file(file)

        # 2. Buat pertanyaan lanjutan untuk Gemini berdasarkan hasil CV
        initial_question = f"Tolong jelaskan secara singkat tentang penyakit '{predicted_class}' pada tanaman cabai dan apa saja gejalanya."
        
        # 3. Dapatkan jawaban yang luwes dari Gemini
        chat_response = get_chatbot_response(initial_question)

        response_data = {
            "status": "success",
            "data": {
                "disease_name": predicted_class,
                "confidence": confidence,
                "initial_response": chat_response
            }
        }
        return jsonify(response_data)
    except Exception as e:
        print(f"[Error] di rute diagnose: {e}")
        return jsonify({"status": "error", "message": "Gagal memproses gambar."}), 500

# Rute baru untuk chat lanjutan
@api_blueprint.route("/api/chat", methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"status": "error", "message": "Pertanyaan tidak ditemukan"}), 400

    try:
        question = data['question']
        chat_response = get_chatbot_response(question)
        return jsonify({"status": "success", "data": {"answer": chat_response}})
    except Exception as e:
        print(f"[Error] di rute chat: {e}")
        return jsonify({"status": "error", "message": "Gagal mendapatkan respons."}), 500