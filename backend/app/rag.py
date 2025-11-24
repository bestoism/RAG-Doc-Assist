import os
from dotenv import load_dotenv
# Embeddings Offline (Gratis & Stabil)
from langchain_huggingface import HuggingFaceEmbeddings
# Chat Online (Google Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
# Loader Dokumen (PDFPlumber untuk hasil bacaan lebih bagus)
from langchain_community.document_loaders import PDFPlumberLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
import shutil 

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(CURRENT_DIR, "..", "chroma_db")

class DocumentProcessor:
    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY tidak ditemukan. Cek file .env")
            
        print("Loading Local Embedding Model... (Download sekali di awal)")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Menggunakan gemini-pro yang stabil
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro", 
            temperature=0.3,
            convert_system_message_to_human=True
        )
        self.vector_store = None

    def process_document(self, file_path: str):
        # --- LANGKAH PEMBERSIHAN ---
        # Hapus database lama agar AI fokus hanya ke file yang BARU saja
        if os.path.exists(CHROMA_PATH):
            try:
                # Paksa hapus folder database
                shutil.rmtree(CHROMA_PATH)
                print("🧹 Memori lama berhasil dibersihkan.")
            except Exception as e:
                print(f"⚠️ Gagal membersihkan memori lama (abaikan jika pertama kali): {e}")
                
        # Reset variable vector_store di memory
        self.vector_store = None
        # ---------------------------

        # Gunakan PDFPlumberLoader agar spasi font tidak berantakan
        if file_path.endswith(".pdf"):
            loader = PDFPlumberLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Format file tidak didukung")
            
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=CHROMA_PATH
        )
        return f"Sukses! Memori direset & {len(splits)} potongan teks baru dipelajari."

    def get_qa_chain(self):
        if not self.vector_store:
            # Load database yang sudah ada jika variable kosong
            self.vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True # Agar kita bisa kembangkan fitur sitasi nanti
        )
        return qa_chain

    # --- INI FUNGSI YANG TADI HILANG ---
    def ask_question(self, query: str):
        chain = self.get_qa_chain()
        # Jalankan chain
        response = chain.invoke({"query": query})
        
        # Ambil hasil jawabannya saja
        return response["result"]
    # -----------------------------------

    def analyze_grammar(self, text: str):
        prompt = f"Analisis tata bahasa (grammar) dari teks berikut. Tunjukkan salahnya dimana dan berikan versi yang benar:\n\n{text}"
        return self.llm.invoke(prompt).content

# Instance global
processor = DocumentProcessor()