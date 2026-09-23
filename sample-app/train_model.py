from __future__ import annotations

import csv
import pickle
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "students.csv"
MODEL_PATH = ROOT / "model.pkl"


def mean(rows: list[dict[str, str]], key: str) -> float:
    return sum(float(row[key]) for row in rows) / len(rows)


def train() -> dict[str, object]:
    with DATA_PATH.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    passing = [row for row in rows if row["passed"] == "1"]
    support = [row for row in rows if row["passed"] == "0"]
    if not passing or not support:
        raise ValueError("training data must contain both classes")

    features = ["study_hours", "attendance", "assignments_completed"]
    scales = {
        "study_hours": 4.0,
        "attendance": 25.0,
        "assignments_completed": 4.0,
    }
    weights = {
        feature: (mean(passing, feature) - mean(support, feature)) / scales[feature]
        for feature in features
    }

    midpoint = {
        feature: (mean(passing, feature) + mean(support, feature)) / 2
        for feature in features
    }
    intercept = -sum(weights[feature] * midpoint[feature] for feature in features)
    return {"intercept": intercept, "weights": weights}


if __name__ == "__main__":
    model = train()
    with MODEL_PATH.open("wb") as stream:
        pickle.dump(model, stream)
    print(f"Created {MODEL_PATH}")

