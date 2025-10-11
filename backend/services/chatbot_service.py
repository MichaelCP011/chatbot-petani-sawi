import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Konfigurasi API Key ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Google API Key: {e}")
    exit()

# --- Definisikan Path ---
VECTOR_STORE_PATH = "backend/knowledge_base/vector_store"

# --- Fungsi untuk Inisialisasi RAG Chain ---
def create_rag_chain():
    """
    Mempersiapkan dan membuat RAG chain yang siap digunakan.
    """
    # 1. Memuat model embedding dan database vektor yang sudah ada
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

    # 2. Membuat retriever dari database vektor
    # Retriever ini bertugas mencari potongan teks yang relevan
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # 3. Membuat model LLM Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    # 4. Membuat template prompt
    # Ini adalah instruksi kita kepada Gemini
    prompt_template = """
    Anda adalah asisten AI ahli pertanian yang ramah dan membantu, bernama "HotBot".
    Tugas Anda adalah menjawab pertanyaan petani mengenai penyakit tanaman cabai berdasarkan konteks dari jurnal penelitian yang diberikan.
    Jawablah pertanyaan hanya berdasarkan konteks berikut:
    
    KONTEKS:
    {context}
    
    PERTANYAAN:
    {question}
    
    JAWABAN:
    """
    prompt = PromptTemplate.from_template(prompt_template)

    # 5. Membuat RAG Chain
    # Ini adalah alur kerja: context -> question -> prompt -> llm -> output
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# --- Fungsi Utama yang akan dipanggil oleh API ---
# Kita inisialisasi chain sekali saja saat modul ini dimuat
rag_chain = create_rag_chain()

def get_chatbot_response(question: str) -> str:
    """
    Menerima pertanyaan, memprosesnya melalui RAG chain, dan mengembalikan jawaban.
    """
    print(f"Menerima pertanyaan: {question}")
    response = rag_chain.invoke(question)
    print(f"Menghasilkan jawaban: {response}")
    return response

# --- Blok untuk Testing Langsung ---
# Anda bisa menjalankan file ini secara langsung untuk menguji fungsinya
if __name__ == '__main__':
    print("Testing chatbot_service.py...")
    
    # Contoh pertanyaan untuk diuji
    test_question_1 = "Apa saja gejala serangan kutu kebul pada tanaman cabai?"
    test_question_2 = "Bagaimana cara mengendalikan penyakit keriting daun secara organik?"
    
    print("\n--- Menjalankan Tes 1 ---")
    answer_1 = get_chatbot_response(test_question_1)
    
    print("\n--- Menjalankan Tes 2 ---")
    answer_2 = get_chatbot_response(test_question_2)

    print("\nPengujian selesai.")