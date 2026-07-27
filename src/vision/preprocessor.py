"""
preprocessor.py — Frame preprocessing before detection.
Owner: DEV1
Input: raw BGR frame from camera
Output: normalized frame ready for detectors
"""
import cv2
import numpy as np
from src.utils.config import get_config


def preprocess(frame: np.ndarray) -> np.ndarray:
    """Resize → denoise → return BGR frame ready for detectors."""
    cfg = get_config()["camera"]
    # Resize to configured resolution
    frame = cv2.resize(frame, (cfg["width"], cfg["height"]))
    # Denoise
    frame = cv2.fastNlMeansDenoisingColored(frame, None, 6, 6, 7, 21)
    return frame
