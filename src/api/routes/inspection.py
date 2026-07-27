"""
inspection.py — POST /api/inspect and GET /api/results endpoints.
Owner: DEV2
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src.db.repository import save_inspection, get_recent

router = APIRouter()


class InspectRequest(BaseModel):
    result: str
    confidence: float
    defect_types: list[str] = []
    shift_id: Optional[str] = None
    operator_id: Optional[str] = None
    batch_id: Optional[str] = None
    defect_regions: list[dict] = []


@router.post("/inspect")
def inspect(req: InspectRequest):
    record = save_inspection(req.model_dump())
    return {"id": record.id, "result": record.result, "confidence": record.confidence}


@router.get("/results")
def results(limit: int = 100):
    records = get_recent(limit)
    return [{"id": r.id, "timestamp": str(r.timestamp),
             "result": r.result, "confidence": r.confidence,
             "defect_types": r.defect_types} for r in records]
