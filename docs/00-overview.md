# 00 · Overview — start here

> **Purpose:** the authoritative navigation doc for this repo. What it is, current state, and where
> everything lives. Read this first, then the numbered docs in order.

## What this is
A **portfolio-grade, education-first** data platform that ingests real public **bike-share** data and
turns it into analytics-ready marts, built the way a senior data engineer would in **2026**:

- **Open lakehouse** — Apache Iceberg tables on object storage (MinIO locally, S3 in the cloud).
- **Data Vault 2.0** integration layer → **Kimball** presentation layer, both in **dbt**.
- **Local-first / $0** — the entire platform runs on a laptop in Docker before any cloud spend.
- **Portable** — the same code promotes to Snowflake / BigQuery / Redshift by swapping an endpoint.

## Current state
**Phase 0 — scaffolding.** Structure + plan only; no pipeline code yet. Build proceeds one phase at a
time, local-first (see [`04-roadmap.md`](04-roadmap.md)).

## The two tracks
- **Local (now):** MinIO + DuckDB + Airflow + dbt, all in Docker, $0.
- **Cloud (opt-in, later):** AWS S3 + Glue + Snowflake/BigQuery/Redshift, added as an overlay in
  [`../cloud/`](../cloud/) — never a fork of this repo.

## Document map
| Doc | What it covers |
|---|---|
| [`01-architecture.md`](01-architecture.md) | Layers, data flow, medallion↔Data-Vault, local→cloud portability |
| [`02-decisions.md`](02-decisions.md) | ADRs — every real choice + its tradeoffs |
| [`03-data-model.md`](03-data-model.md) | Sources (GBFS + trips), DV2.0 hubs/links/sats, Kimball star |
| [`04-roadmap.md`](04-roadmap.md) | Phased build plan (0–9), per-phase purpose, local vs cloud |
| [`05-conventions.md`](05-conventions.md) | File-header rule, dbt naming, commits, LEARNING.md, git flow |
| [`COST.md`](COST.md) | Cost model — local $0; cloud estimates + teardown |
| [`CASE_STUDY.md`](CASE_STUDY.md) | The narrative (problem → architecture → hard decision → result) |
| [`diagrams/`](diagrams/) | Rendered architecture / lineage / DAG / star-schema diagrams |

## Non-goals (deliberately out of scope)
- **Streaming/Kafka** — batch-first keeps the surface small and teachable (may return as a CDC track).
- **Three independent Data Vaults** — the vault is built **once**; see ADR-006.
- **Any PII** — bike-share open data is trip/station level; no personal data is stored.

## Education-first
Every phase ships a `LEARNING.md` (annotated walkthrough — what each tool/command/concept does and
*why*). Code is commented for a learner. See [`05-conventions.md`](05-conventions.md).
