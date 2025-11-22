import streamlit as st
import requests

# Alamat Backend (Pastikan backend jalan di port 8000)
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Doc Assistant", layout="wide")

st.title("🤖 AI Document Assistant")
st.markdown("Upload dokumen (PDF/DOCX), lalu tanyakan apa saja!")

# --- SIDEBAR: UPLOAD FILE ---
with st.sidebar:
    st.header("📂 Upload Dokumen")
    uploaded_file = st.file_uploader("Pilih file PDF atau DOCX", type=['pdf', 'docx'])
    
    if uploaded_file is not None:
        if st.button("Proses Dokumen"):
            with st.spinner("Sedang memproses dokumen ke otak AI..."):
                try:
                    # Kirim file ke Backend
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success("✅ Dokumen berhasil dipelajari!")
                        st.json(response.json())
                    else:
                        st.error(f"Gagal upload: {response.text}")
                except Exception as e:
                    st.error(f"Koneksi Error: {e}")

# --- AREA UTAMA: FITUR ---
tab1, tab2, tab3 = st.tabs(["💬 Chat & Q&A", "📝 Cek Grammar", "📊 Info Project"])

# TAB 1: CHAT
with tab1:
    st.header("Tanya Jawab dengan Dokumen")
    user_query = st.text_input("Apa yang ingin kamu tanyakan tentang dokumen tersebut?")
    
    if st.button("Kirim Pertanyaan"):
        if not user_query:
            st.warning("Tulis pertanyaan dulu dong!")
        else:
            with st.spinner("AI sedang berpikir..."):
                try:
                    payload = {"query": user_query}
                    res = requests.post(f"{API_URL}/chat", json=payload)
                    
                    if res.status_code == 200:
                        answer = res.json().get("answer", "Tidak ada jawaban.")
                        st.markdown("### 🤖 Jawaban AI:")
                        st.write(answer)
                    else:
                        st.error(f"Error Backend: {res.text}")
                except Exception as e:
                    st.error(f"Gagal menghubungi backend: {e}")

# TAB 2: GRAMMAR CHECK
with tab2:
    st.header("Analisis Tata Bahasa")
    text_input = st.text_area("Masukkan kalimat/paragraf yang ingin dicek:")
    
    if st.button("Cek Grammar"):
        if text_input:
            with st.spinner("Menganalisis grammar..."):
                try:
                    res = requests.post(f"{API_URL}/grammar", json={"text": text_input})
                    if res.status_code == 200:
                        st.markdown("### 🔍 Hasil Analisis:")
                        st.write(res.json()['analysis'])
                    else:
                        st.error("Gagal memproses grammar.")
                except Exception as e:
                    st.error(f"Error: {e}")

# TAB 3: INFO
with tab3:
    st.info("Project ini dibuat menggunakan FastAPI (Backend), LangChain (AI Logic), dan Streamlit (Frontend).")
    st.markdown("""
    **Fitur:**
    - RAG (Retrieval Augmented Generation)
    - Upload PDF/DOCX
    - Grammar Check
    - Powered by Google Gemini (Free Tier)
    """)