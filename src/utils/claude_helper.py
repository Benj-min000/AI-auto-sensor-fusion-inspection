"""
claude_helper.py — All Claude API calls go through here.
Owner: CTO
Requires: ANTHROPIC_API_KEY in .env
"""
import os, base64, json
import cv2
import numpy as np

# pip install anthropic
try:
    import anthropic
    _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except ImportError:
    _client = None


def classify_defect(frame: np.ndarray, region: dict) -> dict:
    """Send cropped defect region to Claude for classification."""
    if _client is None:
        return {"type": "unknown", "confidence": 0.0}
    x, y, w, h = region["x"], region["y"], region["w"], region["h"]
    crop = frame[y:y+h, x:x+w]
    _, buf = cv2.imencode(".jpg", crop)
    img_b64 = base64.b64encode(buf).decode()
    resp = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
            {"type": "text", "text": "Classify this manufacturing defect. Respond JSON only: {\"type\": \"scratch|dust|crack|color|ok\", \"confidence\": 0.0-1.0}"}
        ]}]
    )
    return json.loads(resp.content[0].text)


def analyze_root_cause(stats: dict) -> str:
    """Ask Claude to explain why quality problems are happening."""
    if _client is None:
        return "Claude API not configured."
    resp = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content":
            f"Analyze this manufacturing quality data and explain the most likely root cause in 3 bullet points. Data: {json.dumps(stats, indent=2)}"
        }]
    )
    return resp.content[0].text


def generate_shift_report(stats: dict) -> str:
    """Generate a human-readable shift quality report."""
    if _client is None:
        return "Claude API not configured."
    resp = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[{"role": "user", "content":
            f"Write a concise shift quality report for a factory manager. Include: pass rate, top defect types, comparison to previous shift if available, and 2 recommendations. Data: {json.dumps(stats, indent=2)}"
        }]
    )
    return resp.content[0].text
