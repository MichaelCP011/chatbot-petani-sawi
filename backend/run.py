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
    print("[*] Menjalankan server Flask dengan Waitress di http://localhost:5000")
    serve(app, host="0.0.0.0", port=5000)