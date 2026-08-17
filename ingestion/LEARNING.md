# Phase 1 — Ingestion · LEARNING

> **Purpose:** the teaching walkthrough for Phase 1. After reading this you should be able to explain,
> at a senior level, *what* we ingest, *how*, and *why each choice was made* — including the alternatives.

## What Phase 1 does
Fetch real **Capital Bikeshare** data from two sources and land it **unchanged** in the **Bronze** zone
on MinIO (local S3):
1. **GBFS live feed** — `station_information` (slow-changing) + `station_status` (a snapshot of bikes/
   docks available *right now*, `ttl` 60s).
2. **Historical trip files** — monthly ZIPs of completed trips (batch, backfillable).

## The core concepts (be ready to explain these)

### 1. Why land *raw* and *immutable* (Bronze)
We store exactly what the API returned, byte-for-byte, and never edit it. **Why:** if a downstream
transform has a bug, we fix the code and re-run — we never have to re-hit the source (which may have
changed or rate-limited us). Bronze is the **replayable source of truth**.
- *Alternative:* transform-on-ingest (ETL). *Tradeoff:* faster to a first table, but you lose the raw
  history and couple ingestion to your schema assumptions. Modern lakehouses prefer **ELT** (land raw,
  transform later).

### 2. Why *snapshots* build history
GBFS `station_status` only ever tells you **now** — there's no history endpoint. So we **capture a
snapshot on a cadence** and keep every one. Over time those snapshots *become* the history. This is
exactly what a Data Vault **satellite** stores (Phase 3). Key: `bronze/gbfs/<system>/<feed>/dt=YYYY-MM-DD/<feed>_<epoch>.json`.

### 3. Idempotency
Re-running an ingest must be safe. Trip files are content-addressed by month, so we **skip** a file
already landed (`land_trip_file` checks `exists`). Re-running never duplicates or corrupts Bronze.
- *Why it matters:* orchestrators (Airflow, Phase 6) retry tasks; retries must not create duplicates.

### 4. Resilience — retry the right things
`_http.get` retries **only** transient failures — network errors, **429** (rate limited), **5xx**
(server) — with **exponential backoff**. It does **not** retry **4xx** like 404 (a 404 won't fix itself;
retrying wastes time and hammers the source).
- *Alternative:* retry everything / retry nothing. *Tradeoff:* retrying 4xx is pointless and can look
  like abuse; retrying nothing makes you fragile to normal internet blips. Selective retry is the
  senior default. We also honor GBFS `ttl` (60s) — never poll faster than the feed updates.

### 5. Portability (the big one)
Storage is behind a tiny interface (`Storage`), and the S3 client reads its endpoint from **env**. So
`S3Storage` points at **MinIO** locally and **AWS S3** in the cloud with **zero code change** — the
foundation of the "two tracks, one codebase" design (ADR-002).

## How to run it (local)
```bash
make up                       # start MinIO + create the lake bucket
uv run python -m ingestion fetch-gbfs --feeds station_status station_information
uv run python -m ingestion fetch-trips --month 202401
# inspect what landed at the MinIO console: http://localhost:9001
make down
```

## How it's tested (and why that way)
Unit tests mock the HTTP layer (`respx`) and use an **in-memory storage double** — so the whole suite
runs in CI with **no network and no MinIO**: fast, deterministic, free. We test the *contracts* that
matter: retry-on-5xx, no-retry-on-4xx, idempotent landing, correct partition keys.
- *What we deliberately don't unit-test:* the live API and MinIO themselves — that's an integration
  concern (running `make up` + the CLI), not a unit test.

## Senior talking-points from this phase
- "I land **raw and immutable** so ingestion is decoupled from modelling and fully replayable."
- "GBFS has no history, so the pipeline **manufactures** history via cadence snapshots — which is
  precisely what a Data Vault satellite consumes."
- "I retry **429/5xx with backoff** but never 4xx, and honor the feed's `ttl`."
- "Storage is env-driven behind an interface, so **the same code runs on MinIO and S3**."

## Glossary
New terms: *Bronze, immutable, idempotent, exponential backoff, ttl, GBFS, snapshot*. See
[`../docs/GLOSSARY.md`](../docs/GLOSSARY.md).
