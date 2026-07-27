"""
brightness.py — Detects over/under exposure using global stats.
Owner: DEV1
TODO Week 4: implement detect() using mean/std deviation analysis.
"""
import time
import numpy as np
from src.vision.detectors.base import Detector, DetectionResult


class BrightnessDetector(Detector):
    @property
    def name(self) -> str:
        return "brightness"

    def detect(self, frame: np.ndarray) -> DetectionResult:
        start = time.perf_counter()
        # TODO DEV1 Week 4: mean/std detection
        score = 1.0
        duration = (time.perf_counter() - start) * 1000
        return DetectionResult(score=score, defects=[],
                               duration_ms=duration, detector_name=self.name)
