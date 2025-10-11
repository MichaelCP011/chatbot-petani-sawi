# backend/run.py
from flask import Flask
from flask_cors import CORS
from waitress import serve
from api.routes import api_blueprint

# Inisialisasi Aplikasi Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# Konfigurasi CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Daftarkan blueprint API
app.register_blueprint(api_blueprint)

# Menjalankan Aplikasi
if __name__ == "__main__":
    # Ambil port dari environment variable Azure, atau gunakan 5000 jika berjalan lokal
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Menjalankan server di host 0.0.0.0 port {port}")
    serve(app, host="0.0.0.0", port=port)