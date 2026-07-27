"""
root_cause.py — Analytics queries for finding WHY defects happen.
Owner: CTO
Used by pre-ERP monitor and dashboard analytics panel.
"""
from sqlalchemy import text
from src.db.session import get_session


def defect_rate_by_shift(hours: int = 24) -> list[dict]:
    """Which shift has the highest defect rate?"""
    db = get_session()
    try:
        rows = db.execute(text("""
            SELECT shift_id,
                   COUNT(*) as total,
                   SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) as fails,
                   ROUND(100.0 * SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) / COUNT(*), 2) as fail_rate
            FROM inspection_results
            WHERE timestamp >= datetime('now', :h)
            GROUP BY shift_id
            ORDER BY fail_rate DESC
        """), {"h": f"-{hours} hours"}).fetchall()
        return [dict(r._mapping) for r in rows]
    finally:
        db.close()


def defect_rate_by_batch() -> list[dict]:
    """Which material batch causes the most defects?"""
    db = get_session()
    try:
        rows = db.execute(text("""
            SELECT batch_id,
                   COUNT(*) as total,
                   SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) as fails,
                   ROUND(100.0 * SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) / COUNT(*), 2) as fail_rate
            FROM inspection_results
            WHERE batch_id IS NOT NULL
            GROUP BY batch_id
            ORDER BY fail_rate DESC
        """)).fetchall()
        return [dict(r._mapping) for r in rows]
    finally:
        db.close()


def defect_trend_alert(window_minutes: int = 30, threshold: float = 0.15) -> dict:
    """
    PRE-ERP ALERT: if defect rate in last N minutes >= threshold,
    return alert BEFORE ERP sees a batch FAIL.
    """
    db = get_session()
    try:
        r = db.execute(text("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) as fails
            FROM inspection_results
            WHERE timestamp >= datetime('now', :mins)
        """), {"mins": f"-{window_minutes} minutes"}).fetchone()
        total = r.total or 0
        fails = r.fails or 0
        fail_rate = fails / total if total > 0 else 0.0
        if fail_rate >= threshold:
            return {
                "alert": True,
                "fail_rate": round(fail_rate, 4),
                "total_inspected": total,
                "message": f"Defect rate {fail_rate:.1%} in last {window_minutes}min — threshold {threshold:.0%}",
                "action": "HOLD_BATCH",
            }
        return {"alert": False, "fail_rate": round(fail_rate, 4)}
    finally:
        db.close()
