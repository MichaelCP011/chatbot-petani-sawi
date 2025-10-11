import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# --- Konfigurasi API Key ---
# Mengambil API key dari environment variable yang sudah kita set sebelumnya
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    print("Google API Key configured successfully.")
except Exception as e:
    print(f"Error configuring Google API Key: {e}")
    exit()

# --- Definisikan Path ---
# Path ke folder berisi jurnal PDF Anda
JOURNALS_PATH = "backend/knowledge_base/journals"
# Path untuk menyimpan database vektor
VECTOR_STORE_PATH = "backend/knowledge_base/vector_store"


def process_knowledge_base():
    """
    Fungsi untuk memuat, memproses, dan menyimpan knowledge base dari PDF.
    """
    print(f"Memuat dokumen dari {JOURNALS_PATH}...")
    
    # 1. Memuat semua file PDF dari direktori
    loader = PyPDFDirectoryLoader(JOURNALS_PATH)
    documents = loader.load()
    if not documents:
        print("Tidak ada dokumen PDF yang ditemukan. Pastikan file PDF ada di direktori yang benar.")
        return
    print(f"Berhasil memuat {len(documents)} halaman dari semua file PDF.")

    # 2. Memecah dokumen menjadi potongan-potongan teks (chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Ukuran setiap potongan teks
        chunk_overlap=100   # Jumlah tumpang tindih antar potongan
    )
    docs = text_splitter.split_documents(documents)
    print(f"Dokumen dipecah menjadi {len(docs)} potongan teks.")

    # 3. Membuat model embedding
    # Model ini akan mengubah potongan teks menjadi vektor numerik
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # 4. Membuat dan menyimpan database vektor menggunakan FAISS
    print("Membuat database vektor... Proses ini mungkin memakan waktu beberapa menit.")
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # Simpan database vektor ke disk
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Database vektor berhasil dibuat dan disimpan di {VECTOR_STORE_PATH}")


if __name__ == "__main__":
    process_knowledge_base()