from sqlalchemy.orm import Session
from src.db import models
from src.api import schemas

def create_inspection_result(db: Session, inspection: schemas.InspectionResult):
    # Convert Pydantic schema to SQLAlchemy model
    db_inspection = models.InspectionResult(
        result=inspection.result,
        confidence=inspection.confidence,
        defect_types=inspection.defect_types,
        defect_score=inspection.defect_score,
        frame_path=inspection.frame_path,
        shift_id=inspection.shift_id,  # Added for Week 4
        batch_id=inspection.batch_id   # Added for Week 4
    )
    
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection

def get_inspection_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InspectionResult).offset(skip).limit(limit).all()
