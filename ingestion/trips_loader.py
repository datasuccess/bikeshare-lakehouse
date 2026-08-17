# ── ingestion/trips_loader.py ────────────────────────────
# Purpose : download a month of historical trip data (ZIP) and land it raw in Bronze.
# Why     : the batch/backfill counterpart to the live GBFS feed; gives volume + real history.
# Inputs  : base URL + year/month   Outputs: raw ZIP at bronze/trips/<system>/<YYYYMM>-...zip
# Docs    : docs/DATA_SOURCES.md · ingestion/LEARNING.md
from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from . import _http

if TYPE_CHECKING:
    from .storage import Storage

_USER_AGENT = "bikeshare-lakehouse/0.1 (+https://github.com/datasuccess/bikeshare-lakehouse)"


def trip_file_name(year: int, month: int) -> str:
    """Capital Bikeshare monthly file name, e.g. 202401-capitalbikeshare-tripdata.zip."""
    return f"{year:04d}{month:02d}-capitalbikeshare-tripdata.zip"


def land_trip_file(
    storage: Storage,
    base_url: str,
    system_id: str,
    year: int,
    month: int,
    *,
    client: httpx.Client | None = None,
    max_attempts: int = 5,
    backoff: float = 1.0,
    overwrite: bool = False,
) -> str:
    """Download the month's trip ZIP and land it raw. Idempotent: skips if already present."""
    name = trip_file_name(year, month)
    key = f"bronze/trips/{system_id}/{name}"
    if storage.exists(key) and not overwrite:
        return f"skipped (already landed): {key}"

    owns_client = client is None
    client = client or httpx.Client(
        timeout=120.0, follow_redirects=True, headers={"User-Agent": _USER_AGENT}
    )
    try:
        content = _http.get(
            client, f"{base_url}/{name}", max_attempts=max_attempts, backoff=backoff
        ).content
    finally:
        if owns_client:
            client.close()
    return storage.put_bytes(key, content, content_type="application/zip")
