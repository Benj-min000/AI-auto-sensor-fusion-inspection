"""Unit tests for database repository."""
import os, pytest
os.environ["DATABASE_URL"] = "sqlite:///./test_quality.db"

from src.db.repository import save_inspection, get_recent


def test_save_and_retrieve():
    record = save_inspection({
        "result": "PASS",
        "confidence": 0.92,
        "defect_types": [],
        "shift_id": "morning",
        "batch_id": "BATCH-001",
    })
    assert record.id is not None
    assert record.result == "PASS"


def test_get_recent_returns_list():
    results = get_recent(limit=10)
    assert isinstance(results, list)


def teardown_module():
    import os
    if os.path.exists("test_quality.db"):
        os.remove("test_quality.db")
