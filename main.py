"""
main.py — System entry point.
Run inspection loop: camera → detect → decide → save → notify.
Usage: python main.py
"""
import time
from dotenv import load_dotenv
load_dotenv()

from src.vision.capture import Camera
from src.vision.preprocessor import preprocess
from src.vision.detectors.ensemble import Ensemble
from src.db.repository import save_inspection
from src.utils.logger import get_logger

log = get_logger("main")


def run():
    log.info("Starting quality inspection loop")
    ensemble = Ensemble()
    with Camera() as cam:
        if not cam._cap or not cam._cap.isOpened():
            log.error("Camera failed to open. Check USB connection.")
            return
        while True:
            frame = cam.grab_frame()
            if frame is None:
                time.sleep(0.1)
                continue
            processed = preprocess(frame)
            decision = ensemble.run(processed)
            save_inspection({
                "result": decision.result,
                "confidence": decision.confidence,
                "defect_types": [d.defect_type for d in decision.all_defects],
            })
            log.info(f"{decision.result} | score={decision.confidence:.3f} | {decision.total_duration_ms:.1f}ms")


if __name__ == "__main__":
    run()
