"""
config.py — Loads config.yaml into a typed object.
All modules import settings from here. Never read config.yaml directly.
Owner: CTO
"""
import yaml
from pathlib import Path

_cfg = None

def get_config() -> dict:
    global _cfg
    if _cfg is None:
        path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(path) as f:
            _cfg = yaml.safe_load(f)
    return _cfg
