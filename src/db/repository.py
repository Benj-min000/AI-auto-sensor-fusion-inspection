"""
repository.py — All database read/write operations.
Owner: DEV2
No raw SQL here — use SQLAlchemy ORM only.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.models import InspectionResult, DefectRegion
from src.db.session import get_session


def save_inspection(data: dict) -> InspectionResult:
    db: Session = get_session()
    try:
        record = InspectionResult(
            result=data["result"],
            confidence=data["confidence"],
            defect_types=data.get("defect_types", []),
            frame_path=data.get("frame_path"),
            shift_id=data.get("shift_id"),
            operator_id=data.get("operator_id"),
            batch_id=data.get("batch_id"),
            hour_of_day=datetime.utcnow().hour,
        )
        db.add(record)
        db.flush()
        for d in data.get("defect_regions", []):
            db.add(DefectRegion(inspection_id=record.id, **d))
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def get_recent(limit: int = 100) -> list[InspectionResult]:
    db: Session = get_session()
    try:
        return db.query(InspectionResult)\
                 .order_by(InspectionResult.timestamp.desc())\
                 .limit(limit).all()
    finally:
        db.close()
