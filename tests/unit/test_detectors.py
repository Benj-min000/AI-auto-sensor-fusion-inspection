"""Unit tests for detector base classes and ensemble."""
import numpy as np
from src.vision.detectors.base import DetectionResult, DefectRegion
from src.vision.detectors.ensemble import Ensemble


def make_frame(h=800, w=1280):
    return np.zeros((h, w, 3), dtype=np.uint8)


def test_detection_result_score_range():
    result = DetectionResult(score=0.85, detector_name="test")
    assert 0.0 <= result.score <= 1.0


def test_ensemble_returns_valid_result():
    frame = make_frame()
    ensemble = Ensemble()
    result = ensemble.run(frame)
    assert result.result in ("PASS", "WARN", "FAIL")
    assert 0.0 <= result.confidence <= 1.0


def test_ensemble_has_all_scores():
    frame = make_frame()
    ensemble = Ensemble()
    result = ensemble.run(frame)
    assert "surface" in result.scores
    assert "color" in result.scores
    assert "brightness" in result.scores


def test_ensemble_duration_positive():
    frame = make_frame()
    result = Ensemble().run(frame)
    assert result.total_duration_ms >= 0
