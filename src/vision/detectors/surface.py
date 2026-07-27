"""
surface.py — Detects scratches and dust using Canny + morphological analysis.
Owner: DEV1
TODO Week 3: implement detect() using OpenCV Canny edge detection.
"""
import time
import cv2
import numpy as np
from src.vision.detectors.base import Detector, DetectionResult, DefectRegion
from src.utils.config import get_config


class SurfaceDetector(Detector):
    @property
    def name(self) -> str:
        return "surface"

    def detect(self, frame: np.ndarray) -> DetectionResult:
        start = time.perf_counter()
        cfg = get_config()["detectors"]["surface"]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # TODO DEV1 Week 3: implement full Canny + morphological detection here
        # Placeholder — returns perfect score
        defects = []
        score = 1.0

        duration = (time.perf_counter() - start) * 1000
        return DetectionResult(score=score, defects=defects,
                               duration_ms=duration, detector_name=self.name)
