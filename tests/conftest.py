# ── tests/conftest.py ────────────────────────────────────
# Purpose : shared pytest fixtures — the in-memory storage double + a sample GBFS discovery doc.
# Why     : ingestion is unit-tested with NO network and NO MinIO (fast, deterministic CI).
from __future__ import annotations

import pytest
from ingestion.storage import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def gbfs_discovery() -> dict:
    """A minimal GBFS v1.1 discovery document (shape matches Capital Bikeshare)."""
    return {
        "last_updated": 1704067200,
        "ttl": 60,
        "version": "1.1",
        "data": {
            "en": {
                "feeds": [
                    {
                        "name": "station_information",
                        "url": "https://feeds.test/station_information.json",
                    },
                    {"name": "station_status", "url": "https://feeds.test/station_status.json"},
                ]
            }
        },
    }
