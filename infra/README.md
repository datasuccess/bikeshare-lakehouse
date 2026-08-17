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

## MinIO — our local S3 (and how it compares)
**MinIO is an open-source, S3-API-compatible object store you run yourself.** Because it speaks the
same API as AWS S3, the same `boto3` code targets MinIO locally and S3 in the cloud — only
`AWS_ENDPOINT_URL` changes (ADR-002). Its console looks simpler than the AWS S3 console because MinIO
does *one* thing (object storage), while the S3 console is wrapped in all of AWS (IAM, regions,
billing, KMS, storage classes, …). Simpler UI ≠ less capable for our needs.

**Feature parity (most of S3's data-management features exist):**

| Feature | MinIO | AWS S3 |
|---|:---:|:---:|
| Object **versioning** | ✅ | ✅ |
| Object Lock / WORM | ✅ | ✅ |
| Lifecycle (ILM) | ✅ | ✅ |
| Encryption (SSE-S3/KMS/C) | ✅ | ✅ |
| Replication | ✅ | ✅ |
| IAM-style policies / STS | ✅ | ✅ |
| Event notifications | ✅ (webhook/Kafka/…) | ✅ (SNS/SQS/Lambda) |
| S3 Select | ✅ | ✅ |
| Named cold tiers (Glacier) | ❌ (tiers to a remote backend instead) | ✅ |

- **Durability** in MinIO comes from **erasure coding** (data + parity shards across drives/nodes), not
  a managed service. **Storage classes**: MinIO has no Glacier — it lifecycle-transitions cold data to a
  *remote* backend (S3/GCS/Azure/another MinIO).
- **Two layers of versioning in this project:** object versioning (MinIO/S3, versions of a *file*) and
  Iceberg snapshots (Phase 2, versions of a *table*). We lean on the Iceberg layer; Bronze is already
  immutable-by-convention (unique timestamped keys).

## The `make` interface
`make <target>` runs the shell recipe for that target in the root `Makefile` — a documented shortcut
menu (run `make help`). `make up` here is literally `docker compose -f infra/docker-compose.local.yml
up -d`; `make down` stops it. Nothing magic — just one memorable, version-controlled command per task.
