from fastapi.responses import FileResponse
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

# Load the trained model once when the API starts.
MODEL_PATH = Path(__file__).resolve().parent / "linkshield_model.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="LinkShield API",
    description="A machine-learning prototype for URL phishing detection.",
    version="1.0.0",
)

THRESHOLD = 0.5


class PredictRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("URL cannot be blank")

        if any(ord(char) < 32 for char in value):
            raise ValueError("URL cannot contain control characters")

        if not value.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        return value


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": "LinkShield",
        "version": "1.0.0",
    }


@app.post("/api/predict")
def predict(request: PredictRequest):
    probabilities = model.predict_proba([request.url])[0]
    classes = list(model.classes_)

    bad_index = classes.index("bad")
    score = float(probabilities[bad_index])
    prediction = "bad" if score >= THRESHOLD else "good"

    red_flags = []
    url_lower = request.url.lower()

    if "@" in request.url:
        red_flags.append("Contains an @ symbol")

    if request.url.count("-") >= 3:
        red_flags.append("Contains several hyphens")

    if len(request.url) > 100:
        red_flags.append("Unusually long URL")

    if request.url.count(".") >= 4:
        red_flags.append("Contains several dots")

    return {
        "label": prediction,
        "score": round(score, 4),
        "threshold": THRESHOLD,
        "explanation": (
            "The model classified this URL as potentially phishing."
            if prediction == "bad"
            else "The model classified this URL as likely legitimate."
        ),
        "red_flags": red_flags,
        "disclaimer": (
            "This is a machine-learning estimate, not a guarantee. "
            "Do not rely on it alone to decide whether a URL is safe."
        ),
    }
@app.get("/")
def home():
    return FileResponse("public/index.html")