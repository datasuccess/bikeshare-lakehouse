# infra/ — local Docker stack

> **Purpose:** the one-command local environment. Everything the platform needs, containerized, $0.
> **Status:** planned (Phase 0 build). No compose file yet — this README is the spec.

## Planned contents
- `docker-compose.local.yml` — the local stack:
  - **MinIO** — local S3 (Bronze/Silver/Gold buckets + Iceberg warehouse)
  - **Postgres** — Airflow metadata DB (and optional relational Data Vault engine)
  - **Airflow 3** — scheduler + webserver + workers
  - **Iceberg REST catalog** (or Nessie) — catalogs the Iceberg tables
  - **Grafana** — monitoring (Phase 8)
- `Makefile` targets (repo root): `make up` / `make down` / `make run` / `make clean`.

## Why here
Keeps all local-infra concerns in one place and separate from the (later) `cloud/` overlay, so the
default developer experience is 100% local. See [`../docs/01-architecture.md`](../docs/01-architecture.md).
