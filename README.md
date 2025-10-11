# Chatbot Diagnosis Penyakit Tanaman Cabai 🌶️

Sebuah aplikasi web berbasis AI yang berfungsi sebagai asisten virtual bagi petani untuk mendiagnosis penyakit pada tanaman cabai. Aplikasi ini menggunakan model Computer Vision untuk identifikasi awal melalui gambar dan didukung oleh Large Language Model (Google Gemini) untuk sesi tanya jawab yang dinamis dan informatif berdasarkan knowledge base dari jurnal ilmiah.

---

## Fitur Utama

- **Diagnosis Berbasis Gambar:** Unggah gambar daun cabai untuk mendapatkan prediksi penyakit secara real-time.
- **Chatbot Kontekstual:** Ajukan pertanyaan lanjutan dalam bahasa natural untuk mendapatkan penjelasan, cara penanganan, dan pencegahan.
- **Berbasis Pengetahuan Ilmiah:** Jawaban chatbot didasarkan pada kumpulan jurnal penelitian yang relevan menggunakan teknik RAG (Retrieval-Augmented Generation).
- **Antarmuka Web Sederhana:** Mudah digunakan oleh siapa saja, langsung dari browser.

---

## Arsitektur & Alur Kerja Sistem

Sistem ini dibangun dengan arsitektur client-server yang mengintegrasikan beberapa komponen utama: Frontend, Backend, Model CV, dan Layanan LLM.

### Alur Kerja Utama

1. **Inisiasi:** Pengguna membuka aplikasi web. Frontend (HTML/CSS/JS) disajikan oleh Backend (Flask).
2. **Diagnosis Gambar:**
   - Pengguna mengunggah gambar daun cabai.
   - Frontend mengirim gambar ke endpoint `/api/diagnose`.
   - Backend menerima gambar dan Model Computer Vision (TensorFlow/Keras) melakukan prediksi untuk mengidentifikasi penyakit (misal: "leaf curl").
3. **Jawaban Awal (RAG):**
   - Hasil prediksi CV ("leaf curl") diubah menjadi pertanyaan otomatis (misal: "Jelaskan tentang penyakit 'leaf curl'").
   - Pertanyaan ini dikirim ke Layanan Chatbot (Gemini).
   - Sistem RAG mencari konteks paling relevan dari Database Vektor (yang dibuat dari jurnal) dan memberikannya kepada Gemini.
   - Gemini merangkum informasi tersebut menjadi penjelasan awal yang natural.
4. **Tampilan Hasil:**
   - Backend mengembalikan hasil prediksi CV dan penjelasan awal dari Gemini ke Frontend.
   - Frontend menampilkan semua informasi tersebut di jendela chat.
5. **Percakapan Lanjutan:**
   - Pengguna mengetik pertanyaan lanjutan (misal: "Bagaimana cara menanganinya secara organik?").
   - Frontend mengirim pertanyaan ini ke endpoint `/api/chat`.
   - Backend langsung meneruskan pertanyaan ke Layanan Chatbot (langkah 3b & 3c diulang).
   - Jawaban dari Gemini ditampilkan di jendela chat, memungkinkan percakapan yang dinamis.

---

## Teknologi yang Digunakan

- **Backend:** Python, Flask, Waitress (WSGI Server)
- **Frontend:** HTML, CSS, JavaScript
- **Computer Vision:** TensorFlow (Keras), MobileNetV2 (Transfer Learning)
- **Chatbot & NLP:** Google Gemini Pro, LangChain, FAISS (Vector Store)
- **Pemrosesan Data:** PyPDF, NumPy

---

## Instalasi & Penggunaan

Berikut adalah panduan untuk menjalankan proyek ini di lingkungan lokal.

### Prasyarat

- Python 3.9+
- Git

### Langkah-langkah Instalasi

#### 1. Clone Repository

```bash
git clone https://github.com/URL-repository-Anda/nama-repo.git
cd nama-repo
