import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(page_title="AI Doc Assistant", layout="wide", page_icon="🤖")

API_URL = "http://127.0.0.1:8000"

# --- CSS Custom agar tampilan lebih bersih ---
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Judul
st.title("🤖 AI Document Assistant")
st.caption("Powered by RAG + Gemini Pro + Local Embeddings")

# --- SIDEBAR: UPLOAD ---
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
                    st.balloons() # Efek animasi sukses
                else:
                    st.error(f"Gagal: {res.text}")
            except Exception as e:
                st.error(f"Koneksi Error: {e}")

    st.divider()
    st.markdown("### Fitur Lain")
    mode = st.radio("Pilih Mode:", ["💬 Chat Dokumen", "📝 Cek Grammar"])

# --- MODE 1: CHAT DOKUMEN (MODERN UI) ---
if mode == "💬 Chat Dokumen":
    # 1. Inisialisasi History Chat di Memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Tampilkan Chat Terdahulu (biar tidak hilang saat refresh)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Input Chat Baru (Posisinya di bawah)
    if prompt := st.chat_input("Tanyakan sesuatu tentang dokumen..."):
        # Tampilkan pesan User
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Kirim ke Backend & Tampilkan Jawaban AI
        with st.chat_message("assistant"):
            with st.spinner("AI sedang membaca referensi..."):
                try:
                    payload = {"query": prompt}
                    res = requests.post(f"{API_URL}/chat", json=payload)
                    
                    if res.status_code == 200:
                        answer = res.json().get('answer', "Maaf, tidak ada jawaban.")
                        st.markdown(answer)
                        # Simpan jawaban AI ke history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"⚠️ Error dari Backend: {res.text}")
                except Exception as e:
                    st.error(f"🔌 Gagal terhubung ke Backend. Pastikan uvicorn jalan! Error: {e}")

# --- MODE 2: GRAMMAR CHECK ---
elif mode == "📝 Cek Grammar":
    st.subheader("Analisis Tata Bahasa & Ejaan")
    text_input = st.text_area("Masukkan teks yang ingin diperiksa:", height=150)
    
    if st.button("🔍 Periksa Grammar"):
        if text_input:
            with st.spinner("Menganalisis..."):
                try:
                    res = requests.post(f"{API_URL}/grammar", json={"text": text_input})
                    if res.status_code == 200:
                        st.markdown("### Hasil Analisis:")
                        st.info(res.json()['analysis'])
                    else:
                        st.error("Gagal memproses.")
                except Exception as e:
                    st.error(f"Error: {e}")