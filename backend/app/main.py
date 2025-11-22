from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from .rag import processor # Import otak AI kita

app = FastAPI(title="AI Doc Assistant")

# Buat folder sementara untuk simpan file upload
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Model data untuk request
class QueryRequest(BaseModel):
    query: str

class GrammarRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Backend AI RAG Ready!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Simpan file upload ke folder lokal dulu
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Kirim ke otak AI untuk diproses
        msg = processor.process_document(file_location)
        return {"status": "success", "message": msg, "filename": file.filename}
    except Exception as e:
        # Hapus file jika gagal biar bersih
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        answer = processor.ask_question(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grammar")
async def grammar_check(request: GrammarRequest):
    try:
        analysis = processor.analyze_grammar(request.text)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))