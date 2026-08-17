# ── lakehouse/parse.py ───────────────────────────────────
# Purpose : pure functions that turn raw Bronze bytes into Arrow tables (stable schemas).
# Why     : pure = trivially unit-testable; fixed column types keep the Iceberg schema stable so
#           snapshots append cleanly across days/months (docs/03-data-model.md).
# Inputs  : raw bytes + the source file key   Outputs: a pyarrow.Table
# Docs    : lakehouse/LEARNING.md
from __future__ import annotations

import io
import json
import zipfile
from datetime import UTC, datetime

import pyarrow as pa
import pyarrow.csv as pa_csv


def _day(epoch: int) -> str:
    return datetime.fromtimestamp(epoch, tz=UTC).strftime("%Y-%m-%d") if epoch else "1970-01-01"


def _int(value: object) -> int | None:
    return int(value) if value is not None else None


def _float(value: object) -> float | None:
    return float(value) if value is not None else None


def _str(value: object) -> str | None:
    return str(value) if value is not None else None


def parse_station_status(raw: bytes, source_file: str) -> pa.Table:
    """GBFS station_status snapshot -> one row per station (a point-in-time reading)."""
    doc = json.loads(raw)
    snapshot_ts = int(doc.get("last_updated", 0))
    stations = doc.get("data", {}).get("stations", [])
    n = len(stations)
    return pa.table(
        {
            "station_id": pa.array([_str(s.get("station_id")) for s in stations], pa.string()),
            "num_bikes_available": pa.array(
                [_int(s.get("num_bikes_available")) for s in stations], pa.int32()
            ),
            "num_docks_available": pa.array(
                [_int(s.get("num_docks_available")) for s in stations], pa.int32()
            ),
            "num_ebikes_available": pa.array(
                [_int(s.get("num_ebikes_available")) for s in stations], pa.int32()
            ),
            "is_renting": pa.array([_int(s.get("is_renting")) for s in stations], pa.int32()),
            "is_returning": pa.array([_int(s.get("is_returning")) for s in stations], pa.int32()),
            "last_reported": pa.array([_int(s.get("last_reported")) for s in stations], pa.int64()),
            "snapshot_ts": pa.array([snapshot_ts] * n, pa.int64()),
            "dt": pa.array([_day(snapshot_ts)] * n, pa.string()),
            "source_file": pa.array([source_file] * n, pa.string()),
        }
    )


def parse_station_information(raw: bytes, source_file: str) -> pa.Table:
    """GBFS station_information -> one row per station (descriptive attributes)."""
    doc = json.loads(raw)
    snapshot_ts = int(doc.get("last_updated", 0))
    stations = doc.get("data", {}).get("stations", [])
    n = len(stations)
    return pa.table(
        {
            "station_id": pa.array([_str(s.get("station_id")) for s in stations], pa.string()),
            "name": pa.array([_str(s.get("name")) for s in stations], pa.string()),
            "lat": pa.array([_float(s.get("lat")) for s in stations], pa.float64()),
            "lon": pa.array([_float(s.get("lon")) for s in stations], pa.float64()),
            "capacity": pa.array([_int(s.get("capacity")) for s in stations], pa.int32()),
            "region_id": pa.array([_str(s.get("region_id")) for s in stations], pa.string()),
            "snapshot_ts": pa.array([snapshot_ts] * n, pa.int64()),
            "dt": pa.array([_day(snapshot_ts)] * n, pa.string()),
            "source_file": pa.array([source_file] * n, pa.string()),
        }
    )


def parse_trips(zip_bytes: bytes, source_file: str) -> pa.Table:
    """Monthly trips ZIP -> one row per trip. Columns kept as strings (raw layer); types land in
    Silver. Stable string schema also survives the provider's historical schema drift."""
    ym = source_file.rsplit("/", 1)[-1][:6]
    frames: list[pa.Table] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".csv") or name.startswith("__MACOSX"):
                continue
            table = pa_csv.read_csv(io.BytesIO(zf.read(name)))
            table = table.cast(pa.schema([(c, pa.string()) for c in table.column_names]))
            frames.append(table)
    combined = pa.concat_tables(frames)
    n = combined.num_rows
    combined = combined.append_column("ym", pa.array([ym] * n, pa.string()))
    return combined.append_column("source_file", pa.array([source_file] * n, pa.string()))
