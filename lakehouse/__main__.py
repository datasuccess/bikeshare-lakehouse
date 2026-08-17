# ── lakehouse/__main__.py ────────────────────────────────
# Purpose : the CLI — `python -m lakehouse land`.
# Why     : one documented entry point (and later an Airflow task) to build the Iceberg raw layer.
# Docs    : lakehouse/LEARNING.md · Makefile (land target)
from __future__ import annotations

import argparse
from collections.abc import Sequence

from ingestion.config import Settings
from ingestion.storage import S3Storage

from .catalog import load_catalog
from .land import land_all

_TABLES = ["raw_station_status", "raw_station_information", "raw_trips"]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lakehouse", description="Land raw Bronze into Iceberg.")
    sub = parser.add_subparsers(dest="command", required=True)
    land = sub.add_parser("land", help="parse Bronze -> Iceberg tables")
    land.add_argument("--tables", nargs="+", choices=_TABLES, help="subset (default: all)")
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    catalog = load_catalog(settings)
    storage = S3Storage(settings)
    for result in land_all(catalog, storage, settings.system_id, tables=args.tables):
        print(f"{result['table']}: +{result['new_files']} files, {result['rows']} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
