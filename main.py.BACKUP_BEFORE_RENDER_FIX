from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import subprocess
import uuid
from pathlib import Path

app = FastAPI()

# autoriser iPhone
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}.wav"

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ⚠️ adapter le chemin si besoin
        result = subprocess.run(
            ["whisper", str(input_path), "--model", "small", "--language", "fr"],
            capture_output=True,
            text=True
        )

        # récupération texte
        text = result.stdout.strip()

        return {"text": text}

    except Exception as e:
        return {"error": str(e)}


@app.post("/rackscribe")
async def rackscribe(data: dict):
    import json
    import time
    from pathlib import Path

    inbox = Path.home() / "Downloads" / "RackScribe" / "mobile-inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    action_id = data.get("id") or f"MOB{int(time.time() * 1000)}"
    file_path = inbox / f"{action_id}.json"

    payload = {
        "source": "RackScribeMobileVoiceFirst",
        "receivedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": data,
    }

    file_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\n===== RACKSCRIBE MOBILE -> DESKTOP INBOX =====")
    print(file_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("=============================================\n")

    return {
        "status": "ok",
        "savedTo": str(file_path)
    }


# ===== RACKSCRIBE CLOUD QUEUE FINAL =====
CLOUD_QUEUE = []

@app.post("/rackscribe")
async def rackscribe_cloud_queue(data: dict):
    CLOUD_QUEUE.append(data)
    return {
        "status": "ok",
        "mode": "cloud_queue",
        "queue_size": len(CLOUD_QUEUE)
    }

@app.get("/queue")
async def rackscribe_get_queue():
    return {
        "status": "ok",
        "items": CLOUD_QUEUE,
        "queue_size": len(CLOUD_QUEUE)
    }

@app.post("/queue/clear")
async def rackscribe_clear_queue():
    CLOUD_QUEUE.clear()
    return {
        "status": "ok",
        "mode": "queue_cleared"
    }
