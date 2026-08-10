from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

app = FastAPI(title="IndoBERT DANA Sentiment Analysis App")

# 1. Path Folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "indobert_dana")
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# Cek ketersediaan folder model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Folder model tidak ditemukan di: {MODEL_PATH}")

# 2. Load Model & Tokenizer Lokal
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()

# 3. Mount Folder Frontend untuk Aset Statis (CSS & JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

LABEL_MAP = {
    0: "Negatif",
    1: "Netral",
    2: "Positif"
}

class ReviewRequest(BaseModel):
    text: str

# 4. Route Utama: Langsung Menyajikan Halaman Web
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_file_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>File index.html tidak ditemukan di folder frontend</h1>"

# 5. Endpoint API Prediksi
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

    raw_label = model.config.id2label.get(pred_class_id, pred_class_id)
    sentiment_label = LABEL_MAP.get(raw_label, str(raw_label))

    return {
        "text": req.text,
        "sentiment": sentiment_label,
        "confidence": round(confidence * 100, 2)
    }