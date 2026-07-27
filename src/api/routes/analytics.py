"""
analytics.py — Root cause analytics endpoints.
Owner: DEV2 (routes) + CTO (root_cause queries)
"""
from fastapi import APIRouter
from src.analytics.root_cause import defect_rate_by_shift, defect_rate_by_batch, defect_trend_alert

router = APIRouter()

@router.get("/by-shift")
def by_shift(hours: int = 24):
    return defect_rate_by_shift(hours)

@router.get("/by-batch")
def by_batch():
    return defect_rate_by_batch()

@router.get("/trend-alert")
def trend_alert(window: int = 30, threshold: float = 0.15):
    return defect_trend_alert(window, threshold)
