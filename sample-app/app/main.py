from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .model import load_model, predict_probability


MODEL_VERSION = os.environ.get("MODEL_VERSION", "v1")
MODEL_PATH = Path(os.environ.get("MODEL_PATH", "/app/model.pkl"))
if not MODEL_PATH.exists():
    MODEL_PATH = Path(__file__).resolve().parents[1] / "model.pkl"

model = load_model(MODEL_PATH)
app = FastAPI(
    title="Student Success Prediction API",
    description="Workshop API demonstrating Docker and Kubernetes deployment.",
    version=MODEL_VERSION,
)


class PredictionRequest(BaseModel):
    study_hours: float = Field(ge=0, le=24, examples=[7])
    attendance: float = Field(ge=0, le=100, examples=[85])
    assignments_completed: int = Field(ge=0, le=10, examples=[8])


class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    model_version: str


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Student Success Prediction API",
        "docs": "/docs",
        "model_version": MODEL_VERSION,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    probability = predict_probability(
        model,
        study_hours=request.study_hours,
        attendance=request.attendance,
        assignments_completed=request.assignments_completed,
    )
    return PredictionResponse(
        prediction="pass" if probability >= 0.5 else "needs-support",
        probability=round(probability, 4),
        model_version=MODEL_VERSION,
    )

