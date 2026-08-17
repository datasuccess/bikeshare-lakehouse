# ── ingestion/__main__.py ────────────────────────────────
# Purpose : the CLI — `python -m ingestion fetch-gbfs|fetch-trips`.
# Why     : one documented entry point for humans and (later) Airflow tasks.
# Docs    : ingestion/LEARNING.md · Makefile (ingest-* targets)
from __future__ import annotations

import argparse
from collections.abc import Sequence

from .config import Settings
from .gbfs_client import GbfsClient, land_gbfs_snapshot
from .storage import S3Storage
from .trips_loader import land_trip_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ingestion", description="Land raw bike-share data in Bronze."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("fetch-gbfs", help="snapshot GBFS feeds into Bronze")
    g.add_argument("--feeds", nargs="+", default=["station_information", "station_status"])

    t = sub.add_parser("fetch-trips", help="land a month of historical trip data")
    t.add_argument("--month", required=True, help="YYYYMM, e.g. 202401")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    settings = Settings.from_env()
    storage = S3Storage(settings)

    if args.command == "fetch-gbfs":
        client = GbfsClient(settings.gbfs_discovery_url)
        for feed in args.feeds:
            uri = land_gbfs_snapshot(client, storage, feed, settings.system_id)
            print(f"landed {feed} -> {uri}")
    elif args.command == "fetch-trips":
        year, month = int(args.month[:4]), int(args.month[4:6])
        print(land_trip_file(storage, settings.trips_base_url, settings.system_id, year, month))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
