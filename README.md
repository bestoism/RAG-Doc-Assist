# 📄 AI Document Assistant (Context-Aware RAG)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg) ![LangChain](https://img.shields.io/badge/LangChain-0.3.7-orange.svg) ![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)

An intelligent, full-stack document analysis tool powered by **Retrieval-Augmented Generation (RAG)**. This project allows users to upload PDF or DOCX files and have a **context-aware conversation** with them. It uses a **Hybrid AI approach** (Local Embeddings + Cloud LLM) to ensure speed, stability, and zero cost.

---
<img width="1919" height="852" alt="image" src="https://github.com/user-attachments/assets/68b311b3-035f-493b-885b-e25b6fd626f0" />
---

## 🚀 Key Features (Updated)

*   **🗣️ Conversational Memory:** The AI remembers previous context in the chat, allowing for natural follow-up questions (e.g., "Who is the author?" -> "How old is he?").
*   **🔍 Source Citations:** Every answer comes with expandable source references, showing exactly which file and page the information was pulled from.
*   **📚 Smart Parsing:** Uses `pdfplumber` to accurately read complex PDF layouts, tables, and unconventional fonts.
*   **⚡ Hybrid AI Engine:**
    *   **Embeddings:** Runs locally using HuggingFace (`all-MiniLM-L6-v2`) — *Unlimited & Private*.
    *   **LLM:** Powered by **Google Gemini (Flash/Pro)** — *Fast & High Quality*.
*   **🐳 Dockerized:** Fully containerized with Docker and Docker Compose for easy deployment.
*   **🧹 Auto-Reset Memory:** Automatically clears the vector database when a new file is uploaded to prevent data contamination.
*   **📝 Grammar Analysis:** A dedicated tool to check and correct grammar in texts.

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Stable version for AI/ML libraries. |
| **Backend** | FastAPI | REST API to handle file uploads & logic. |
| **Frontend** | Streamlit | Interactive Chat UI with history state. |
| **Orchestration** | LangChain | Framework for RAG & Contextual Rephrasing. |
| **Vector DB** | ChromaDB | Local database to store text embeddings. |
| **Parsing** | PDFPlumber | Advanced PDF text extraction. |
| **Deployment** | Docker | Containerization for reproducible builds. |

---

## 📦 Installation & Setup

You can run this project either **Manually** (Local Environment) or using **Docker**.

### Option 1: Manual Setup (Local)

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/rag-doc-assistant.git
    cd rag-doc-assistant
    ```

2.  **Create Virtual Environment (Python 3.11 Recommended)**
    ```bash
    # Windows
    py -3.11 -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    ```

4.  **Configure API Key**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

5.  **Run the App (Two Terminals Needed)**
    *   Terminal 1 (Backend): `uvicorn backend.app.main:app --reload`
    *   Terminal 2 (Frontend): `streamlit run frontend/app.py`

---

### Option 2: Docker Setup (Recommended) 🐳

Ensure you have **Docker Desktop** installed and running.

1.  **Configure API Key**
    Create a `.env` file in the root directory with your `GOOGLE_API_KEY`.

2.  **Build and Run**
    ```bash
    docker-compose up --build
    ```

3.  **Access the App**
    Open your browser at: `http://localhost:8501`

---

## 🔮 Project Roadmap & Status

| Feature | Status | Description |
| :--- | :--- | :--- |
| **RAG Core** | ✅ Completed | PDF Upload + Vector DB + LLM Answer. |
| **Grammar Check** | ✅ Completed | Separate tab for linguistic analysis. |
| **Conversational Memory** | ✅ Completed | Backend rephrases queries based on history. |
| **Source Citations** | ✅ Completed | UI displays page numbers for verification. |
| **Docker Support** | ✅ Completed | `Dockerfile` and `docker-compose` added. |
| **Smart PDF Parsing** | ✅ Completed | Integrated `pdfplumber` for better OCR-like reading. |
| **Multi-File Support** | 🚧 Planned | Allow querying multiple PDFs simultaneously. |
| **Table Extraction** | 🚧 Planned | Extract data tables to CSV/Excel. |
| **Cloud Deployment** | 🚧 Planned | Deploy to Streamlit Cloud / Railway / AWS. |

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
