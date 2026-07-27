"""
main.py — FastAPI application entry point.
Owner: DEV2
Runs: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.routes import inspection, analytics, erp
from src.analytics.root_cause import defect_trend_alert
from src.utils.logger import get_logger

log = get_logger(__name__)
app = FastAPI(title="AI Quality Platform", version="1.0.0")

# ── Routes ────────────────────────────────────────────
app.include_router(inspection.router, prefix="/api")
app.include_router(analytics.router, prefix="/api/analytics")
app.include_router(erp.router, prefix="/api/erp")

# ── WebSocket manager ─────────────────────────────────
class WSManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except Exception:
                pass

ws_manager = WSManager()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()   # keep alive
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)


@app.get("/")
async def dashboard():
    return FileResponse("src/dashboard/index.html")


@app.on_event("startup")
async def startup():
    asyncio.create_task(pre_erp_monitor())
    log.info("API started — pre-ERP monitor running")


async def pre_erp_monitor():
    """Check defect trend every 5 minutes — alert ERP before batch fails."""
    while True:
        try:
            alert = defect_trend_alert()
            if alert["alert"]:
                await ws_manager.broadcast({"type": "PRE_ERP_ALERT", **alert})
                log.warning(f"Pre-ERP alert triggered: {alert['message']}")
        except Exception as e:
            log.error(f"Monitor error: {e}")
        await asyncio.sleep(300)
