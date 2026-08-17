# ── lakehouse/catalog.py ─────────────────────────────────
# Purpose : build the Iceberg REST catalog client from Settings.
# Why     : the REST protocol is what AWS Glue speaks too, so local↔cloud is the same client
#           with a different URI (ADR-006). MinIO needs path-style S3 + an explicit endpoint.
# Docs    : lakehouse/LEARNING.md · infra/docker-compose.local.yml (iceberg-rest service)
from __future__ import annotations

from typing import TYPE_CHECKING

from pyiceberg.catalog.rest import RestCatalog

if TYPE_CHECKING:
    from ingestion.config import Settings


def load_catalog(settings: Settings) -> RestCatalog:
    """Connect to the Iceberg REST catalog, with S3/MinIO file IO configured."""
    return RestCatalog(
        "local",
        uri=settings.catalog_uri,
        warehouse=settings.warehouse,
        **{
            "s3.endpoint": settings.endpoint_url,
            "s3.access-key-id": settings.access_key,
            "s3.secret-access-key": settings.secret_key,
            "s3.region": settings.region,
            "s3.path-style-access": "true",
        },
    )
