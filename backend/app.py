from flask import Flask

# Membuat instance aplikasi Flask
app = Flask(__name__)

# Membuat sebuah "endpoint" atau "rute" sederhana
# Ini seperti mendefinisikan alamat URL untuk diakses
@app.route("/")
def hello_world():
    return "Backend chatbot aktif!"

# Baris ini memastikan server hanya berjalan saat file ini dieksekusi langsung
if __name__ == "__main__":
    app.run(debug=True)