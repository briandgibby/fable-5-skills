"""Deprecated: JSON settings loader.

Kept for reference after the 1.0 packaging change moved runtime
configuration into src/defaults.py. No module imports this anymore.
"""
import json
from pathlib import Path


def load_settings():
    path = Path(__file__).resolve().parents[1] / "config" / "settings.json"
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
