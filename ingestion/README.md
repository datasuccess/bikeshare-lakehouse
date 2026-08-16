# ingestion/ — source loaders

> **Purpose:** fetch real public bike-share data and land it **unchanged** in Bronze on MinIO.
> **Status:** planned (Phase 1). Spec only.

## Planned contents
- `gbfs_client.py` — GBFS feed reader (`station_information`, `station_status`, `free_bike_status`).
  High-cadence **snapshots**; resilient to rate limits (backoff), pagination, transient 5xx.
- `trips_loader.py` — downloads + lands monthly historical **trip CSV** dumps (batch, backfillable).
- `landing.py` — writes raw payloads to `bronze/…` on MinIO with `record_source` + `load_datetime`.

## Principles
- **Raw is immutable** — Bronze stores exactly what the source returned (replayable).
- **Endpoint from env** — `AWS_ENDPOINT_URL` points at MinIO locally, S3 in the cloud (unchanged code).
- **Idempotent** — re-running a fetch for the same batch window is a no-op.

Resilience patterns are inspired by the `cmc-crypto` reference repo and rewritten for GBFS (ADR-009).
See [`../docs/03-data-model.md`](../docs/03-data-model.md).
