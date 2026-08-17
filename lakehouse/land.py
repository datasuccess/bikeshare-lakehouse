# ── lakehouse/land.py ────────────────────────────────────
# Purpose : read new Bronze objects, parse them, and append into Iceberg tables (idempotently).
# Why     : Bronze is raw files; this makes them queryable, versioned tables. Idempotency = we
#           track which source files a table already holds and skip them, so re-runs are safe.
# Inputs  : a pyiceberg Catalog + a Storage      Outputs: rows appended; a per-table summary
# Docs    : lakehouse/LEARNING.md
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import pyarrow as pa
from pyiceberg.transforms import IdentityTransform

from .parse import parse_station_information, parse_station_status, parse_trips

if TYPE_CHECKING:
    from ingestion.storage import Storage
    from pyiceberg.catalog import Catalog

ParseFn = Callable[[bytes, str], pa.Table]


def _loaded_source_files(catalog: Catalog, ident: str) -> set[str]:
    """Source-file keys already present in the table (empty if it doesn't exist yet)."""
    if not catalog.table_exists(ident):
        return set()
    arrow = catalog.load_table(ident).scan(selected_fields=("source_file",)).to_arrow()
    return set(arrow.column("source_file").to_pylist()) if arrow.num_rows else set()


def _append(catalog: Catalog, ident: str, data: pa.Table, partition_col: str) -> None:
    namespace = ident.split(".")[0]
    catalog.create_namespace_if_not_exists(namespace)
    if not catalog.table_exists(ident):
        table = catalog.create_table(ident, schema=data.schema)
        with table.update_spec() as update:  # partition by day/month (Iceberg hidden partitioning)
            update.add_field(partition_col, IdentityTransform(), partition_col)
    catalog.load_table(ident).append(data)


def land_table(
    catalog: Catalog,
    storage: Storage,
    *,
    table: str,
    prefix: str,
    suffix: str,
    parse_fn: ParseFn,
    partition_col: str,
    namespace: str = "bronze",
) -> dict[str, object]:
    """Append every not-yet-loaded Bronze object under ``prefix`` into ``namespace.table``."""
    ident = f"{namespace}.{table}"
    loaded = _loaded_source_files(catalog, ident)
    keys = [k for k in storage.list_keys(prefix) if k.endswith(suffix) and k not in loaded]
    if not keys:
        return {"table": ident, "new_files": 0, "rows": 0}
    data = pa.concat_tables([parse_fn(storage.get_bytes(k), k) for k in keys])
    _append(catalog, ident, data, partition_col)
    return {"table": ident, "new_files": len(keys), "rows": data.num_rows}


def land_all(
    catalog: Catalog,
    storage: Storage,
    system_id: str,
    *,
    tables: list[str] | None = None,
) -> list[dict[str, object]]:
    """Land the three raw tables (or the subset named in ``tables``)."""
    specs: dict[str, dict] = {
        "raw_station_status": {
            "prefix": f"bronze/gbfs/{system_id}/station_status/",
            "suffix": ".json",
            "parse_fn": parse_station_status,
            "partition_col": "dt",
        },
        "raw_station_information": {
            "prefix": f"bronze/gbfs/{system_id}/station_information/",
            "suffix": ".json",
            "parse_fn": parse_station_information,
            "partition_col": "dt",
        },
        "raw_trips": {
            "prefix": f"bronze/trips/{system_id}/",
            "suffix": ".zip",
            "parse_fn": parse_trips,
            "partition_col": "ym",
        },
    }
    chosen = tables or list(specs)
    return [land_table(catalog, storage, table=name, **specs[name]) for name in chosen]
