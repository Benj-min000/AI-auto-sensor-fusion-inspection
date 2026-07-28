from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db import models

router = APIRouter()

@router.get("/stats/shift")
def get_shift_stats(db: Session = Depends(get_db)):
    """Calculates total inspections, fails, and defect rate per shift."""
    inspections = db.query(models.InspectionResult).all()
    
    stats = {}
    for insp in inspections:
        # Fallback to 'Unknown' if shift_id wasn't provided
        shift = insp.shift_id or "Unknown" 
        
        if shift not in stats:
            stats[shift] = {"total": 0, "fails": 0}
        
        stats[shift]["total"] += 1
        if insp.result == "FAIL":
            stats[shift]["fails"] += 1
            
    # Calculate the defect rate percentage for each shift
    for shift, data in stats.items():
        if data["total"] > 0:
            data["defect_rate_percent"] = round((data["fails"] / data["total"]) * 100, 2)
        else:
            data["defect_rate_percent"] = 0.0
            
    return stats

# for mr Jun to merge his code and swap out the mock string for the real API call.
@router.get("/stats/root-cause")
def get_root_cause_analysis(db: Session = Depends(get_db)):
    """
    Provides an AI-generated root cause analysis.
    Note: Currently using simulated logic until Jun's claude_helper.py is merged.
    """
    # Fetch the stats using the function we already wrote
    stats = get_shift_stats(db)
    
    # Simulate Claude's analysis based on our test data
    night_rate = stats.get("night", {}).get("defect_rate_percent", 0)
    
    if night_rate > 50:
        analysis = f"Claude Analysis: ⚠️ The 'night' shift is showing a critical defect rate of {night_rate}%. The primary defect type observed is 'scratch'. Recommendation: Inspect the conveyor belt for sharp debris and verify operator handling procedures for BATCH-999."
    else:
        analysis = "Claude Analysis: ✅ Quality metrics are within normal parameters across all shifts. No significant anomalies detected."
        
    return {"analysis": analysis}
