from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
MODEL_PATH = BASE_DIR / "indobert_dana"
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(title="IndoBERT DANA Sentiment Analysis App")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Folder model tidak ditemukan: {MODEL_PATH}")

try:
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH), local_files_only=True)
    model.eval()
except Exception as e:
    raise RuntimeError(f"Gagal memuat model IndoBERT dari {MODEL_PATH}. Pastikan folder model valid. Error: {e}")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
else:
    print(f"Peringatan: folder frontend tidak ditemukan: {FRONTEND_DIR}")

LABEL_MAP = {0: "Negatif", 1: "Netral", 2: "Positif"}

class ReviewRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_file_path = FRONTEND_DIR / "index.html"
    if html_file_path.exists():
        return html_file_path.read_text(encoding="utf-8")
    return "<h1>File index.html tidak ditemukan di folder frontend</h1>"

@app.post("/predict")
def predict_sentiment(req: ReviewRequest):
    inputs = tokenizer(
        req.text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        pred_class_id = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_class_id].item()

    sentiment_label = LABEL_MAP.get(pred_class_id, str(pred_class_id))

    return {
        "text": req.text,
        "sentiment": sentiment_label,
        "confidence": round(confidence * 100, 2)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)