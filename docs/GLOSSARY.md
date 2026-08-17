# Glossary

> **Purpose:** the vocabulary of this project in plain language, so you can *speak* it fluently. Terms
> are grouped; each is one sentence + why it matters here.

## Lakehouse & storage
- **Lakehouse** — a data lake (cheap object storage) with database-like table features (ACID, schema,
  time-travel) on top; here via Iceberg on MinIO/S3.
- **Object storage** — files addressed by key in buckets (S3/MinIO), not a database; cheap and scalable.
- **MinIO** — an open-source, S3-API-compatible object store; our **local** stand-in for AWS S3.
- **Apache Iceberg** — an open table format that makes a pile of Parquet files behave like a versioned
  SQL table; portable across engines (the key to local↔cloud).
- **Parquet** — a columnar file format; efficient for analytics scans.
- **Catalog** — the registry that maps table names → their Iceberg metadata/files.

## Medallion (data quality zones)
- **Bronze** — raw, immutable landing of exactly what the source returned; replayable.
- **Silver** — cleansed + integrated data; here modelled as the Data Vault.
- **Gold** — curated, consumer-ready marts; here the Kimball star schema.

## Data Vault 2.0 (the integration layer)
- **Hub** — the distinct list of a business key (e.g. `station_id`) + its hash key.
- **Link** — a relationship between hubs (e.g. a trip: start-station × end-station × bike).
- **Satellite** — descriptive attributes + their change history, attached to a hub or link.
- **Business key** — the natural identifier a business uses (station id), stable across sources.
- **Hash key** — a deterministic hash of the business key; the surrogate join key in the vault.
- **Hashdiff** — a hash of a satellite's attributes; if it changes, the row changed → store new version.
- **Append-only** — never update/delete; new versions are appended (full auditable history).

## Kimball (the presentation layer)
- **Fact** — a table of measurable events at a defined **grain** (e.g. one row per trip).
- **Dimension** — the descriptive context you filter/group by (station, date, member type).
- **Grain** — exactly what one fact row represents; the first thing to nail in a star schema.
- **SCD2 (slowly changing dimension type 2)** — keeps history by adding a new dim row on change.
- **Conformed dimension** — a dimension shared consistently across multiple facts.

## Pipeline & operations
- **GBFS** — General Bikeshare Feed Specification; the standardized real-time bike-share feed.
- **Idempotent** — running it twice yields the same result as once (safe re-runs).
- **Backfill** — loading historical periods after the fact.
- **Exponential backoff** — waiting progressively longer between retries of a failing call.
- **TTL** — "time to live"; how long a feed value is valid (GBFS says 60s) — don't poll faster.
- **DAG** — directed acyclic graph; Airflow's model of tasks + dependencies.
- **Freshness / SLA** — how recent the data is vs. the target we commit to.
- **Data contract** — an enforced agreement on a dataset's schema/semantics.
- **Lineage** — the traced path of data from source to mart.
- **OIDC** — short-lived, keyless cloud auth (vs. long-lived access keys).
