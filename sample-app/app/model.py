from __future__ import annotations

import math
import pickle
from pathlib import Path
from typing import TypedDict


class ModelData(TypedDict):
    intercept: float
    weights: dict[str, float]


def load_model(path: Path) -> ModelData:
    with path.open("rb") as stream:
        model = pickle.load(stream)
    if not isinstance(model, dict) or "intercept" not in model or "weights" not in model:
        raise ValueError("model.pkl has an invalid format")
    return model


def predict_probability(
    model: ModelData,
    study_hours: float,
    attendance: float,
    assignments_completed: int,
) -> float:
    weights = model["weights"]
    score = (
        model["intercept"]
        + weights["study_hours"] * study_hours
        + weights["attendance"] * attendance
        + weights["assignments_completed"] * assignments_completed
    )
    return 1.0 / (1.0 + math.exp(-score))

