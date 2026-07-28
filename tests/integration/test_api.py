from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_inspect_and_get_results():
    # 1. Post a new inspection result
    payload = {
        "result": "FAIL",
        "confidence": 0.85,
        "defect_types": ["scratch"],
        "defect_score": 0.6,
        "frame_path": "/archive/test_fail_01.jpg",
        "shift_id": "night",
        "batch_id": "BATCH-999"
    }
    
    post_response = client.post("/api/inspect", json=payload)
    assert post_response.status_code == 200
    post_data = post_response.json()
    assert post_data["shift_id"] == "night"
    
    # 2. Get the results and verify our created entry is there
    get_response = client.get("/api/results")
    assert get_response.status_code == 200
    
    results = get_response.json()
    assert len(results) > 0
    
    # Check if our specific batch is in the returned list
    batch_ids = [r.get("batch_id") for r in results]
    assert "BATCH-999" in batch_ids
