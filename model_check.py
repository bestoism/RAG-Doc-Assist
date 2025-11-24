import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key tidak ditemukan di .env")
else:
    print(f"✅ API Key ditemukan: {api_key[:5]}...")
    
    try:
        genai.configure(api_key=api_key)
        print("\n🔍 Sedang mencari model yang tersedia untukmu...")
        
        available_models = []
        for m in genai.list_models():
            # Kita cari model yang bisa 'generateContent' (untuk Chat)
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("\n⚠️ Tidak ada model yang ditemukan. Cek apakah API Key sudah aktif di Google AI Studio?")
    except Exception as e:
        print(f"\n❌ Error Koneksi: {e}")