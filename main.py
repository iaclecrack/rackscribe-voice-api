from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pathlib import Path

app = FastAPI()

# Autoriser iPhone / mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ===== TEST ROUTE =====
@app.get("/")
async def root():
    return {"status": "ok", "message": "RackScribe API running"}

# ===== TRANSCRIBE (temporaire simplifié pour test) =====
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return {"text": "test transcription ok"}

# ===== CLOUD QUEUE =====
CLOUD_QUEUE = []

@app.post("/rackscribe")
async def push_order(data: dict):
    CLOUD_QUEUE.append(data)
    return {"status": "queued", "queue_size": len(CLOUD_QUEUE)}

@app.get("/queue")
async def get_queue():
    return {"items": CLOUD_QUEUE}

@app.post("/queue/clear")
async def clear_queue():
    CLOUD_QUEUE.clear()
    return {"status": "cleared"}
