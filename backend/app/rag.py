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
from langchain.prompts import PromptTemplate

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

        # Gunakan PDFPlumberLoader agar spasi font tidak berantakan
        if file_path.endswith(".pdf"):
            loader = PDFPlumberLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Format file tidak didukung")
            
        docs = loader.load()
        
        print(f"📄 Total Halaman: {len(docs)}")
        if len(docs) > 0:
            print("🔍 Intip Halaman 1 (Cover):")
            print(docs[0].page_content[:500])

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
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 10})
        
        template = """Kamu adalah asisten dokumen yang cerdas.
        Gunakan potongan konteks berikut untuk menjawab pertanyaan di akhir.
        Jika kamu tidak tahu jawabannya dari konteks, katakan saja "Maaf, informasi tersebut tidak ditemukan dalam dokumen ini", jangan mencoba mengarang jawaban.
        
        Konteks:
        {context}
        
        Pertanyaan: {question}
        
        Jawaban yang Bermanfaat:"""
        
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True # Agar kita bisa kembangkan fitur sitasi nanti
        )
        return qa_chain

    # ... (kode atas tetap sama) ...

    # Ubah definisi fungsi ini untuk menerima history
    def ask_question(self, query: str, history: list = []):
        
        # 1. CONTEXTUAL REPHRASING (Jika ada history)
        final_query = query
        
        if history:
            # Format history menjadi teks string
            chat_history_str = ""
            for chat in history[-4:]: # Ambil 4 chat terakhir saja biar hemat
                role = "User" if chat['role'] == 'user' else "Assistant"
                chat_history_str += f"{role}: {chat['content']}\n"
            
            # Minta LLM memperbaiki pertanyaan (Rephrasing)
            prompt_rephrase = f"""
            Berdasarkan riwayat percakapan berikut, ubah pertanyaan user menjadi pertanyaan lengkap yang bisa berdiri sendiri.
            Jangan jawab pertanyaannya, cukup tulis ulang pertanyaannya agar jelas subjeknya.
            
            Riwayat:
            {chat_history_str}
            
            Pertanyaan User: {query}
            
            Pertanyaan Baru (Lengkap):"""
            
            # Pakai LLM untuk mikir sebentar
            rephrased = self.llm.invoke(prompt_rephrase).content
            print(f"🔄 Rephrasing: '{query}' -> '{rephrased}'") # Cek di terminal
            final_query = rephrased

        # 2. Cari Jawaban pakai Query yang sudah diperbaiki
        chain = self.get_qa_chain()
        response = chain.invoke({"query": final_query})
        
        # 3. Format Output
        answer_text = response["result"]
        source_documents = response["source_documents"]
        list_sumber = []
        
        for doc in source_documents:
            page_num = doc.metadata.get("page", 0) + 1
            file_name = os.path.basename(doc.metadata.get("source", "Dokumen"))
            list_sumber.append(f"{file_name} (Hal. {page_num})")
        
        unique_sources = list(set(list_sumber))
        
        return {
            "answer": answer_text,
            "sources": unique_sources,
            "debug_query": final_query # Dikirim balik biar kita tahu (opsional)
        }

    def analyze_grammar(self, text: str):
        prompt = f"Analisis tata bahasa (grammar) dari teks berikut. Tunjukkan salahnya dimana dan berikan versi yang benar:\n\n{text}"
        return self.llm.invoke(prompt).content

# Instance global
processor = DocumentProcessor()