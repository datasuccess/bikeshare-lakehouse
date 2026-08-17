# ── tests/test_trips_loader.py ───────────────────────────
# Purpose : correct monthly file name + idempotent landing (second call skips the download).
from __future__ import annotations

import httpx
import respx
from ingestion.trips_loader import land_trip_file, trip_file_name


def test_trip_file_name():
    assert trip_file_name(2024, 1) == "202401-capitalbikeshare-tripdata.zip"


def test_land_trip_file_is_idempotent(storage):
    url = "https://trips.test/202401-capitalbikeshare-tripdata.zip"
    with respx.mock:
        route = respx.get(url).mock(return_value=httpx.Response(200, content=b"ZIPDATA"))

        uri = land_trip_file(storage, "https://trips.test", "dca-cabi", 2024, 1, backoff=0)
        msg = land_trip_file(storage, "https://trips.test", "dca-cabi", 2024, 1, backoff=0)

        assert uri == "mem://bronze/trips/dca-cabi/202401-capitalbikeshare-tripdata.zip"
        assert msg.startswith("skipped")
        assert route.call_count == 1  # second call short-circuited (idempotent)
