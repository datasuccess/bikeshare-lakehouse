# ── ingestion/config.py ──────────────────────────────────
# Purpose : all runtime settings, read from the environment (12-factor).
# Why     : same code targets MinIO locally and S3 in cloud — only env changes (ADR-002).
# Inputs  : environment variables (see .env.example)   Outputs: an immutable Settings object
# Docs    : docs/01-architecture.md
from __future__ import annotations

import os
from dataclasses import dataclass

# Capital Bikeshare (dca-cabi) defaults — works out-of-the-box locally (docs/DATA_SOURCES.md).
_DEFAULT_GBFS = "https://gbfs.capitalbikeshare.com/gbfs/gbfs.json"
_DEFAULT_TRIPS = "https://s3.amazonaws.com/capitalbikeshare-data"


@dataclass(frozen=True)
class Settings:
    """Immutable ingestion settings. Build with :meth:`from_env`."""

    endpoint_url: str
    access_key: str
    secret_key: str
    region: str
    bucket: str
    gbfs_discovery_url: str
    system_id: str
    trips_base_url: str
    catalog_uri: str

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            endpoint_url=os.environ.get("AWS_ENDPOINT_URL", "http://localhost:9000"),
            access_key=os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin"),
            secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin"),
            region=os.environ.get("AWS_REGION", "us-east-1"),
            bucket=os.environ.get("LAKE_BUCKET", "bikeshare-lake"),
            gbfs_discovery_url=os.environ.get("GBFS_DISCOVERY_URL", _DEFAULT_GBFS),
            system_id=os.environ.get("SYSTEM_ID", "dca-cabi"),
            trips_base_url=os.environ.get("TRIPS_BASE_URL", _DEFAULT_TRIPS),
            catalog_uri=os.environ.get("CATALOG_URI", "http://localhost:8181"),
        )

    @property
    def warehouse(self) -> str:
        """Iceberg warehouse location on the object store (bucket-relative)."""
        return f"s3://{self.bucket}/warehouse"
