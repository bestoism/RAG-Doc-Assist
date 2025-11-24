# Gunakan Python 3.11 Slim (Ringan)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements dan install
COPY backend/requirements.txt backend/requirements.txt
COPY frontend/requirements.txt frontend/requirements.txt

# Install dependencies (gabung backend & frontend biar simpel di 1 container)
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Copy semua kode
COPY . .

# Expose port (8000 backend, 8501 frontend)
EXPOSE 8000 8501

# Script untuk menjalankan keduanya bersamaan (Entrypoint sederhana)
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0