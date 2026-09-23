from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model import load_model, predict_probability


def test_high_engagement_predicts_pass() -> None:
    model = load_model(ROOT / "model.pkl")
    probability = predict_probability(model, 8, 90, 9)
    assert probability >= 0.5


def test_low_engagement_needs_support() -> None:
    model = load_model(ROOT / "model.pkl")
    probability = predict_probability(model, 2, 55, 3)
    assert probability < 0.5

