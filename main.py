from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import uuid
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QUEUE_FILE = Path("cloud_queue.json")

def load_queue():
    try:
        if QUEUE_FILE.exists():
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []

def save_queue(items):
    QUEUE_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

@app.get("/")
async def root():
    return {"status": "ok", "message": "RackScribe cloud API running"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Version cloud stable temporaire : transcription cloud désactivée
    return {
        "status": "ok",
        "text": "facture client test 1 produit test 1 euro",
        "mode": "cloud_stable_test"
    }

@app.post("/rackscribe")
async def rackscribe_queue(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    item = {
        "cloudId": "CLOUD-" + str(uuid.uuid4()),
        "receivedAt": datetime.datetime.now().isoformat(),
        "data": data
    }

    queue = load_queue()
    queue.append(item)
    save_queue(queue)

    return {"status": "ok", "mode": "queued", "queue_size": len(queue)}

@app.get("/queue")
async def get_queue():
    queue = load_queue()
    return {"status": "ok", "items": [x.get("data", x) for x in queue], "queue_size": len(queue)}

@app.post("/queue/clear")
async def clear_queue():
    save_queue([])
    return {"status": "ok", "mode": "cleared"}
