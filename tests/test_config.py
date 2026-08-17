# ── tests/test_config.py ─────────────────────────────────
# Purpose : Settings reads sane defaults and honors env overrides (12-factor).
from __future__ import annotations

from ingestion.config import Settings

_ENV = [
    "AWS_ENDPOINT_URL",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_REGION",
    "LAKE_BUCKET",
    "GBFS_DISCOVERY_URL",
    "SYSTEM_ID",
    "TRIPS_BASE_URL",
]


def test_defaults(monkeypatch):
    for key in _ENV:
        monkeypatch.delenv(key, raising=False)
    settings = Settings.from_env()
    assert settings.system_id == "dca-cabi"
    assert settings.gbfs_discovery_url.endswith("gbfs.json")
    assert settings.bucket == "bikeshare-lake"


def test_env_override(monkeypatch):
    monkeypatch.setenv("LAKE_BUCKET", "custom-bucket")
    monkeypatch.setenv("SYSTEM_ID", "nyc")
    settings = Settings.from_env()
    assert settings.bucket == "custom-bucket"
    assert settings.system_id == "nyc"
