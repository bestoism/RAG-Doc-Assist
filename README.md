# 📄 AI Document Assistant (RAG + Grammar Analysis)
An intelligent, full-stack document analysis tool powered by **Retrieval-Augmented Generation (RAG)**. This project allows users to upload PDF or DOCX files and chat with them to extract insights, summaries, and specific information. It uses a **Hybrid AI approach** (Local Embeddings + Cloud LLM) to ensure speed, stability, and zero cost.


![Python](https://img.shields.io/badge/Python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg) ![LangChain](https://img.shields.io/badge/LangChain-0.3.7-orange.svg) ![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg)

<img width="997" height="628" alt="image" src="https://github.com/user-attachments/assets/7a629a1c-18d2-4e45-a054-6d9f1d158c0c" />
---
<img width="1588" height="782" alt="image" src="https://github.com/user-attachments/assets/69860c05-940f-43ab-9c4b-54ede11b2d41" />

## 🚀 Key Features

*   **📚 Chat with Documents (RAG):** Upload any PDF or DOCX and ask questions based on its content.
*   **🧠 Smart Parsing:** Uses `pdfplumber` to accurately read complex PDF layouts, preventing garbled text issues.
*   **⚡ Hybrid AI Engine:**
    *   **Embeddings:** Runs locally using HuggingFace (`all-MiniLM-L6-v2`) — *Unlimited & Private*.
    *   **LLM:** Powered by **Google Gemini Pro** — *Fast & High Quality*.
*   **📝 Grammar Analysis:** A dedicated tool to check and correct grammar in texts.
*   **💾 Persistent Memory:** Uses **ChromaDB** to store document vectors locally.
*   **🖥️ Modern UI:** Built with **Streamlit** for a clean and interactive user experience.
*   **⚙️ Robust Backend:** Built with **FastAPI** for high-performance API handling.

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Stable version for AI/ML libraries. |
| **Backend** | FastAPI | REST API to handle file uploads & logic. |
| **Frontend** | Streamlit | User Interface for file upload & chat. |
| **Orchestration** | LangChain | Framework for connecting LLMs and Data. |
| **Vector DB** | ChromaDB | Local database to store text embeddings. |
| **LLM** | Google Gemini Pro | The intelligence engine (via API). |
| **Embeddings** | HuggingFace | Local model for text-to-vector conversion. |

---

## 📦 Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/rag-doc-assistant.git
cd rag-doc-assistant
```

### 2. Create a Virtual Environment
**Recommended:** Use **Python 3.11** to avoid compatibility issues with NumPy/ChromaDB.
```bash
# Windows
py -3.11 -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install Backend & AI libraries
pip install -r backend/requirements.txt

# Install Frontend libraries
pip install -r frontend/requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/)):

```env
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ How to Run

You need to run the Backend and Frontend in **two separate terminals**.

### Terminal 1: Backend (API)
```bash
uvicorn backend.app.main:app --reload
```
*Server will start at `http://127.0.0.1:8000`*

### Terminal 2: Frontend (UI)
```bash
streamlit run frontend/app.py
```
*The App will open in your browser at `http://localhost:8501`*

---

## 🔮 Project Roadmap (Future Improvements)

Here are some ideas for future development to make this project even better:

- [ ] **Conversational Memory:** Add history support so the AI remembers previous questions in the chat session.
- [ ] **Multi-File Support:** Allow users to upload multiple PDFs at once and query across all of them.
- [ ] **Table Extraction:** Create a specific feature to extract tables from PDFs and export them to CSV/Excel.
- [ ] **Source Citations:** Make the AI show exactly which page or paragraph the answer came from.
- [ ] **Dockerization:** Create a `Dockerfile` and `docker-compose.yml` for one-click deployment.
- [ ] **User Authentication:** Add login functionality to save user documents privately.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🚧 This project is under construction — stay tuned for more updates!
