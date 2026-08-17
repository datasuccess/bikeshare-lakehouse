# Phase 2 — Lakehouse landing · LEARNING

> **Purpose:** the teaching walkthrough for Phase 2. After this you can explain, at a senior level, how
> raw files in a bucket become **Apache Iceberg tables** — and why that unlocks schema, snapshots, and
> time-travel.

## What Phase 2 does
Read the raw Bronze objects and append them into **Iceberg tables** on MinIO, via **pyiceberg**,
cataloged by an **Iceberg REST catalog**:
- `bronze.raw_station_status` — one row per station per snapshot (history accumulates here)
- `bronze.raw_station_information` — one row per station (attributes)
- `bronze.raw_trips` — one row per historical trip

## The core concepts (be ready to explain these)

### 1. Table format vs. raw files — what Iceberg *adds*
Bronze is just files in a bucket. A **table format** (Iceberg) puts a metadata layer over those Parquet
files so they behave like a real SQL table:
- **Schema** — named, typed columns (not "hope the JSON matches").
- **ACID commits** — an append either fully happens or doesn't; readers never see a half-write.
- **Snapshots / time-travel** — every commit creates a new *snapshot*; you can query the table *as of*
  any past snapshot.
- **Hidden partitioning** — the table knows its partitioning; queries prune automatically.
- **Schema evolution** — add/rename/drop columns without rewriting data.
- *Alternatives:* Delta Lake, Hudi. Iceberg won on openness + multi-engine support (every warehouse
  reads it) — the reason our Phase 9 cloud engines can all read the *same* tables.

### 2. The catalog — turning files into named tables
A **catalog** maps `bronze.raw_trips` → the current metadata file. We run an **Iceberg REST catalog**
locally because that's the same protocol **AWS Glue** speaks — so Phase 9 swaps the catalog URI, not the
code (ADR-006). MinIO needs `s3.path-style-access` + an explicit endpoint (see `lakehouse/catalog.py`).

### 3. Snapshots = table versioning (we proved it)
We captured two `station_status` snapshots and the table went **860 → 1,720 rows across 2 snapshots**;
time-travelling to snapshot 1 returned exactly **860**. This is the *table*-level history — distinct
from MinIO object versioning (a *file*'s versions). GBFS only serves "now"; **snapshots are how we
manufacture history** for the Data Vault satellites in Phase 3.

### 4. Hidden partitioning
`station_status`/`station_information` are partitioned by **`dt`** (day), `trips` by **`ym`** (month).
Iceberg records the partition in metadata, so a query like "Feb 2025 trips" prunes to just that
partition — you don't add a `WHERE` on a derived column. At dev scale it barely matters; the habit and
mechanism are what count.

### 5. Idempotency
Each row carries its `source_file`. Before landing, we read the set of `source_file`s already in the
table and skip them — so `make land` twice in a row is a **no-op** (we verified `+0 files`). Re-runs are
safe, which matters once Airflow (Phase 6) retries tasks.

### 6. Raw stays faithful (esp. trips)
Trip columns are kept as **strings** in this raw layer — types are assigned later in Silver. That also
means the provider's real **schema drift** (legacy `Duration/…` vs current `ride_id/…`) lands without
breaking, which we deliberately exploit in the Phase 8 chaos drill.

## How to run it (local)
```bash
make up                      # MinIO + Iceberg REST catalog
make ingest-gbfs             # (Phase 1) land raw snapshots in Bronze
make ingest-trips MONTH=202502
make land                    # Bronze -> Iceberg tables
```
The REST-catalog fixture keeps state **in memory** — after `make down`/restart, re-run `make land`
(Bronze itself persists in MinIO's volume).

## How it's tested (and why that way)
Unit tests use **pyiceberg's SQLite catalog on a temp dir** + the in-memory storage double — real
Iceberg tables created on the local filesystem, **no Docker/MinIO/network**. We test the contracts:
parsers produce stable schemas; landing is idempotent; new files become new snapshots; partitioning is
applied.

## Senior talking-points from this phase
- "Iceberg turns a pile of Parquet into a **versioned SQL table** — schema, ACID, snapshots, evolution."
- "I run a **REST catalog** locally because it's the same protocol as **Glue**, so cloud is a URI swap."
- "**Snapshots** give me table-level time-travel; that's how I turn a live-only feed into history."
- "Landing is **idempotent** via `source_file` tracking, so retries and re-runs are safe."
- "Raw trips stay **string-typed** so the source's schema drift can't break the load."

## Glossary
New/related terms: *Iceberg, catalog, snapshot, time-travel, partitioning, schema evolution,
idempotent*. See [`../docs/GLOSSARY.md`](../docs/GLOSSARY.md).
