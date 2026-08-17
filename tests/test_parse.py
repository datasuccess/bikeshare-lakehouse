# ── tests/test_parse.py ──────────────────────────────────
# Purpose : the pure Bronze->Arrow parsers produce the right rows, columns, and stable types.
from __future__ import annotations

import io
import json
import zipfile

import pyarrow as pa
from lakehouse.parse import parse_station_information, parse_station_status, parse_trips


def _status_bytes() -> bytes:
    return json.dumps(
        {
            "last_updated": 1704067200,  # 2024-01-01 UTC
            "ttl": 60,
            "data": {
                "stations": [
                    {"station_id": "S1", "num_bikes_available": 5, "num_docks_available": 3},
                    {"station_id": "S2", "num_bikes_available": 0, "num_docks_available": 8},
                ]
            },
        }
    ).encode()


def test_parse_station_status():
    table = parse_station_status(_status_bytes(), "bronze/…/f.json")
    assert table.num_rows == 2
    assert table.column("station_id").to_pylist() == ["S1", "S2"]
    assert table.column("num_bikes_available").to_pylist() == [5, 0]
    assert table.column("dt").to_pylist() == ["2024-01-01", "2024-01-01"]
    assert {"snapshot_ts", "source_file"} <= set(table.column_names)


def test_parse_station_information():
    raw = json.dumps(
        {
            "last_updated": 1704067200,
            "data": {"stations": [{"station_id": "S1", "name": "Main St", "capacity": 15}]},
        }
    ).encode()
    table = parse_station_information(raw, "k.json")
    assert table.num_rows == 1
    assert table.column("name").to_pylist() == ["Main St"]
    assert table.column("capacity").to_pylist() == [15]


def _trips_zip() -> bytes:
    csv = b"ride_id,rideable_type,member_casual\nR1,classic,member\nR2,electric,casual\n"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("202401-capitalbikeshare-tripdata.csv", csv)
    return buffer.getvalue()


def test_parse_trips_keeps_strings_and_adds_partition():
    table = parse_trips(_trips_zip(), "bronze/trips/dca-cabi/202401-capitalbikeshare-tripdata.zip")
    assert table.num_rows == 2
    assert table.column("ride_id").to_pylist() == ["R1", "R2"]
    assert table.column("ym").to_pylist() == ["202401", "202401"]
    # raw layer keeps every source column as a string (types are assigned in Silver)
    assert table.schema.field("rideable_type").type == pa.string()
