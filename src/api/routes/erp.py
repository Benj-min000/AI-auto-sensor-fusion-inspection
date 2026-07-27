"""
erp.py — Outbound ERP webhook.
Owner: CTO
Sends QUALITY_WARNING to ERP when pre-ERP monitor triggers.
"""
import httpx
from fastapi import APIRouter
from src.utils.config import get_config
from src.utils.logger import get_logger

router = APIRouter()
log = get_logger(__name__)


async def send_erp_webhook(payload: dict):
    cfg = get_config()["erp"]
    if not cfg["enabled"]:
        log.info(f"ERP disabled — would have sent: {payload}")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.post(cfg["webhook_url"], json=payload, timeout=5.0)
        log.info(f"ERP webhook: {resp.status_code}")
