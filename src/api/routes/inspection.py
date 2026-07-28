from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.api import schemas
from src.db import repository

router = APIRouter()

@router.post("/inspect", response_model=schemas.InspectionResult)
def inspect_part(inspection: schemas.InspectionResult, db: Session = Depends(get_db)):
    # Connect POST /inspect to save the result to the DB
    db_inspection = repository.create_inspection_result(db, inspection)
    return db_inspection

@router.get("/results", response_model=List[schemas.InspectionResult])
def get_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Write GET /results endpoint to query saved data
    results = repository.get_inspection_results(db, skip=skip, limit=limit)
    return results
