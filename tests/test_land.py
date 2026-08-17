# ── tests/test_land.py ───────────────────────────────────
# Purpose : landing is idempotent and each new source file becomes a new Iceberg snapshot.
# Why     : proves the real land logic against a real Iceberg catalog — no Docker/MinIO, using
#           pyiceberg's SQLite catalog on a temp dir.
from __future__ import annotations

import json

import pytest
from ingestion.storage import InMemoryStorage
from lakehouse.land import land_table
from lakehouse.parse import parse_station_status
from pyiceberg.catalog.sql import SqlCatalog

_PREFIX = "bronze/gbfs/dca-cabi/station_status/"


@pytest.fixture
def catalog(tmp_path):
    warehouse = tmp_path / "wh"
    warehouse.mkdir()
    return SqlCatalog(
        "test", uri=f"sqlite:///{tmp_path}/catalog.db", warehouse=f"file://{warehouse}"
    )


def _status(ts: int) -> bytes:
    return json.dumps(
        {"last_updated": ts, "data": {"stations": [{"station_id": "S1", "num_bikes_available": 5}]}}
    ).encode()


def _land(catalog, storage):
    return land_table(
        catalog,
        storage,
        table="raw_station_status",
        prefix=_PREFIX,
        suffix=".json",
        parse_fn=parse_station_status,
        partition_col="dt",
    )


def test_land_is_idempotent_and_snapshots_accumulate(catalog):
    storage = InMemoryStorage()
    storage.put_bytes(f"{_PREFIX}dt=2024-01-01/station_status_1704067200.json", _status(1704067200))

    first = _land(catalog, storage)
    assert first["new_files"] == 1 and first["rows"] == 1

    again = _land(catalog, storage)  # nothing new -> no-op
    assert again["new_files"] == 0

    # a new snapshot file -> a new Iceberg snapshot, history grows
    storage.put_bytes(f"{_PREFIX}dt=2024-01-02/station_status_1704153600.json", _status(1704153600))
    third = _land(catalog, storage)
    assert third["new_files"] == 1

    table = catalog.load_table("bronze.raw_station_status")
    assert table.scan().to_arrow().num_rows == 2
    assert len(list(table.snapshots())) == 2
    assert [f.name for f in table.spec().fields] == ["dt"]  # partitioned by day
