from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

class ResultState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"

class InspectionResult(BaseModel):
    result: ResultState
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0")
    defect_types: List[str] = Field(default_factory=list, description="List of defects")
    defect_score: float = Field(..., description="Calculated severity score")
    frame_path: str = Field(..., description="File path to the archived image frame")
    
    shift_id: Optional[str] = None
    batch_id: Optional[str] = None
    
    # Modern Pydantic V2 syntax
    model_config = ConfigDict(from_attributes=True)
