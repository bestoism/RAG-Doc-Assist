import streamlit as st
import requests

st.set_page_config(page_title="AI Doc Assistant", layout="wide", page_icon="🤖")

API_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Document Assistant")
st.caption("Powered by RAG + Gemini Pro + Local Embeddings")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📂 Upload Dokumen")
    uploaded_file = st.file_uploader("Upload PDF / DOCX", type=['pdf', 'docx'])
    
    if uploaded_file and st.button("Proses Dokumen"):
        with st.spinner("Sedang membaca & mengingat isi dokumen..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                res = requests.post(f"{API_URL}/upload", files=files)
                if res.status_code == 200:
                    st.success("✅ Sukses! Dokumen berhasil dipelajari.")
                    # Reset history chat saat upload file baru
                    st.session_state.messages = []
                else:
                    st.error(f"Gagal: {res.text}")
            except Exception as e:
                st.error(f"Koneksi Error: {e}")

    st.divider()
    mode = st.radio("Pilih Mode:", ["💬 Chat Dokumen", "📝 Cek Grammar"])

# --- MODE 1: CHAT DOKUMEN ---
if mode == "💬 Chat Dokumen":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 1. LOOP RENDERING (Tampilkan Chat Lama + Sumbernya)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # --- PERBAIKAN: Tampilkan sumber jika ada di history ---
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sumber Referensi (History)"):
                    for s in message["sources"]:
                        st.caption(f"• {s}")
            # -------------------------------------------------------

    # 2. INPUT USER
    if prompt := st.chat_input("Tanyakan sesuatu... (Made by Besto)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Kirim ke Backend & Tampilkan Jawaban AI
        with st.chat_message("assistant"):
            with st.spinner("AI sedang mengingat konteks & membaca..."):
                try:
                    # --- PERUBAHAN DISINI ---
                    # Siapkan history (buang key 'sources' biar ringan, ambil role & content aja)
                    clean_history = [
                        {"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages
                    ]
                    
                    # Kirim query + history
                    payload = {"query": prompt, "history": clean_history}
                    res = requests.post(f"{API_URL}/chat", json=payload)
                    # ------------------------
                    
                    if res.status_code == 200:
                        data = res.json()
                        answer_text = data.get('answer', "Maaf, tidak ada jawaban.")
                        sources = data.get('sources', [])
                        
                        st.markdown(answer_text)
                        
                        if sources:
                            with st.expander("📚 Sumber Referensi"):
                                for s in sources:
                                    st.caption(f"• {s}")
                        
                        # Simpan ke history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer_text,
                            "sources": sources
                        })
                    else:
                        st.error(f"⚠️ Error dari Backend: {res.text}")
                except Exception as e:
                    st.error(f"🔌 Gagal terhubung ke Backend. Pastikan uvicorn jalan! Error: {e}")

# --- MODE 2: GRAMMAR ---
elif mode == "📝 Cek Grammar":
    st.subheader("Analisis Tata Bahasa")
    text = st.text_area("Masukkan teks:", height=150)
    if st.button("Periksa"):
        if text:
            with st.spinner("Menganalisis..."):
                res = requests.post(f"{API_URL}/grammar", json={"text": text})
                if res.status_code == 200:
                    st.info(res.json()['analysis'])