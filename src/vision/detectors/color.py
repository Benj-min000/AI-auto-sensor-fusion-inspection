"""
color.py — Detects color anomalies using HSV range analysis.
Owner: DEV1
TODO Week 4: implement detect() using OpenCV HSV thresholding.
"""
import time
import numpy as np
from src.vision.detectors.base import Detector, DetectionResult


class ColorDetector(Detector):
    @property
    def name(self) -> str:
        return "color"

    def detect(self, frame: np.ndarray) -> DetectionResult:
        start = time.perf_counter()
        # TODO DEV1 Week 4: HSV anomaly detection
        score = 1.0
        duration = (time.perf_counter() - start) * 1000
        return DetectionResult(score=score, defects=[],
                               duration_ms=duration, detector_name=self.name)
