# -*- coding: utf-8 -*-

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from .inference import reorder_model


class FeaturesRequest(BaseModel):
    features: Dict[str, float]


class PredictionResponse(BaseModel):
    probability: float
    label: int
    threshold: float


app = FastAPI(title="Instacart Reorder API", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: FeaturesRequest) -> PredictionResponse:
    proba, label = reorder_model.predict(request.features)
    return PredictionResponse(
        probability=proba,
        label=label,
        threshold=reorder_model.threshold,
    )
