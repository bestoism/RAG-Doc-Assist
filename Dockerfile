# 1. Gunakan Python 3.11 (Versi Stabil yang kita pakai)
FROM python:3.11-slim

# 2. Set folder kerja di dalam container
WORKDIR /app

# 3. Copy file requirements dulu (biar cache-nya awet)
COPY backend/requirements.txt backend/requirements.txt
COPY frontend/requirements.txt frontend/requirements.txt

# 4. Install semua library sekaligus
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# 5. Copy seluruh kode project ke dalam container
COPY . .

# (Opsional) Beritahu port mana yang akan dipakai
EXPOSE 8000
EXPOSE 8501