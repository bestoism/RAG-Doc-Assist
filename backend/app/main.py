from fastapi import FastAPI

app = FastAPI(title="AI Doc Assistant")

@app.get("/")
def read_root():
    return {"message": "Halo! Backend AI Document Assistant sudah aktif 🚀"}