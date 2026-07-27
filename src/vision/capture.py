"""
capture.py — Camera initialization and frame capture.
Owner: DEV1
Camera: Arducam UC852 (OV9782) — USB 2.0, no driver needed.
"""
import cv2
import numpy as np
from src.utils.config import get_config
from src.utils.logger import get_logger

log = get_logger(__name__)


class Camera:
    def __init__(self):
        cfg = get_config()["camera"]
        self.device_id = cfg["device_id"]
        self.width = cfg["width"]
        self.height = cfg["height"]
        self.fps = cfg["fps"]
        self._cap = None

    def open(self) -> bool:
        self._cap = cv2.VideoCapture(self.device_id, cv2.CAP_DSHOW)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._cap.set(cv2.CAP_PROP_FPS, self.fps)
        ok = self._cap.isOpened()
        log.info(f"Camera opened: {ok} | {self.width}x{self.height} @ {self.fps}fps")
        return ok

    def grab_frame(self) -> np.ndarray | None:
        if self._cap is None or not self._cap.isOpened():
            log.error("Camera not open")
            return None
        ret, frame = self._cap.read()
        if not ret:
            log.warning("Failed to grab frame")
            return None
        return frame

    def release(self):
        if self._cap:
            self._cap.release()
            log.info("Camera released")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *_):
        self.release()
