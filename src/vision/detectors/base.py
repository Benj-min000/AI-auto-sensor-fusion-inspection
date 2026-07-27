"""
base.py — Abstract base class for all detectors.
Owner: CTO
All detectors (surface, color, brightness) must inherit from Detector.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np


@dataclass
class DefectRegion:
    x: int
    y: int
    w: int
    h: int
    confidence: float
    defect_type: str   # 'scratch' | 'dust' | 'color' | 'brightness'


@dataclass
class DetectionResult:
    score: float                          # 0.0 = bad, 1.0 = perfect
    defects: list[DefectRegion] = field(default_factory=list)
    duration_ms: float = 0.0
    detector_name: str = ""


class Detector(ABC):
    @abstractmethod
    def detect(self, frame: np.ndarray) -> DetectionResult:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
