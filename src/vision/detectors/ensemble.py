"""
ensemble.py — Combines all detector scores into final PASS/FAIL/WARN.
Owner: CTO
TODO Week 4: wire up all detectors and apply weighted scoring.
"""
import numpy as np
from src.vision.detectors.base import DetectionResult
from src.vision.detectors.surface import SurfaceDetector
from src.vision.detectors.color import ColorDetector
from src.vision.detectors.brightness import BrightnessDetector
from src.utils.config import get_config
from dataclasses import dataclass, field


@dataclass
class EnsembleResult:
    result: str          # 'PASS' | 'WARN' | 'FAIL'
    confidence: float    # 0.0 – 1.0
    scores: dict = field(default_factory=dict)
    all_defects: list = field(default_factory=list)
    total_duration_ms: float = 0.0


class Ensemble:
    def __init__(self):
        self.detectors = [
            SurfaceDetector(),
            ColorDetector(),
            BrightnessDetector(),
        ]

    def run(self, frame: np.ndarray) -> EnsembleResult:
        cfg = get_config()
        weights = cfg["decision"]["weights"]
        pass_t = cfg["decision"]["pass_threshold"]
        warn_t = cfg["decision"]["warn_threshold"]

        scores = {}
        all_defects = []
        total_ms = 0.0

        for detector in self.detectors:
            result = detector.detect(frame)
            scores[detector.name] = result.score
            all_defects.extend(result.defects)
            total_ms += result.duration_ms

        # Weighted combined score
        combined = sum(scores[n] * weights.get(n, 0) for n in scores)

        if combined >= pass_t:
            verdict = "PASS"
        elif combined >= warn_t:
            verdict = "WARN"
        else:
            verdict = "FAIL"

        return EnsembleResult(
            result=verdict,
            confidence=combined,
            scores=scores,
            all_defects=all_defects,
            total_duration_ms=total_ms,
        )
