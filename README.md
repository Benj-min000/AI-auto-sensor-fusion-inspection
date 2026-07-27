<<<<<<< HEAD
# AI Manufacturing Quality Platform

**Automotive parts quality inspection — Detection → Root Cause → Pre-ERP Alert**

## Stack
- **Vision**: Python 3.10 + OpenCV (→ C++17 in Phase 2)
- **API**: FastAPI + WebSocket
- **DB**: SQLite (→ PostgreSQL in production)
- **AI**: Claude API (Anthropic)
- **Camera**: Arducam UC852 (OV9782 color global shutter, USB 2.0)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in .env
cp .env.example .env

# 3. Test camera first
python test_camera.py

# 4. Run inspection loop
python main.py

# 5. Run API server (separate terminal)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Run tests
pytest tests/ -v
```

## Project Structure
```
quality_platform/
├── cpp/                    # C++ vision layer (Phase 2)
├── src/
│   ├── vision/             # Camera + detectors (DEV1)
│   ├── decision/           # PASS/FAIL engine (CTO)
│   ├── analytics/          # Root cause engine (CTO)
│   ├── db/                 # Database layer (DEV2)
│   ├── api/                # FastAPI server (DEV2)
│   └── utils/              # Config, logger, Claude
├── tests/                  # All tests
├── claude_prompts/         # Saved Claude prompts
├── config.yaml             # All thresholds — tune here
└── main.py                 # Entry point
```

## Roles
- 🔵 **CTO**: Architecture, CI/CD, root cause engine, Claude integration
- 🟢 **DEV1**: Vision algorithms, camera pipeline, test fixtures
- 🟡 **DEV2**: Database, FastAPI, dashboard, ERP webhook

## 8-Week MVP
| Week | Milestone |
|------|-----------|
| W1 | Camera live, dev environment |
| W2 | Vision pipeline core |
| W3 | Surface defect detector |
| W4 | Color + ensemble + full loop |
| W5 | Root cause analytics engine |
| W6 | Live dashboard + WebSocket |
| W7 | Pre-ERP alert + Claude reports |
| W8 | Production hardening + CI/CD |
=======
# AI-auto-sensor-fusion-inspection
>>>>>>> 0b18daef00fb2c70aaacbf18815ea6d52e05196b
