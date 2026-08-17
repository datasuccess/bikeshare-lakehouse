# 04 · Roadmap

> **Purpose:** the phased build plan. Each phase has a single clear purpose and ships working code +
> a `LEARNING.md`. **Phases 0–8 are 100% local / $0. Phase 9 is the opt-in cloud promotion.** Built
> one phase at a time; nothing starts until the previous phase runs end-to-end.

## Legend
`✅ done` · `🔵 in progress` · `⚪ planned` · 🏠 local ($0) · ☁️ cloud (opt-in, paid)

## Phases
| # | Phase | 🏠/☁️ | What it delivers | Purpose (the story it tells) | Status |
|---|-------|:---:|------------------|------------------------------|:---:|
| **0** | Foundations | 🏠 | Docker stack (MinIO, Postgres, Airflow, catalog), CI, pre-commit, docs, conventions | reproducible $0 stack + hygiene from commit #1 | ✅ |
| **1** | Ingestion | 🏠 | API clients (GBFS + trip files) with retry / backoff / pagination → Bronze on MinIO | real-data credibility + resilience | ✅ |
| **2** | Lakehouse landing | 🏠 | Bronze → **Iceberg** on MinIO (pyiceberg + local REST catalog) | real Iceberg-on-S3 mechanics at $0 | ✅ |
| **3** | Data Vault 2.0 | 🏠 | dbt: hubs / links / satellites (hash keys, hashdiff, idempotent) | auditable, source-agnostic history | ⚪ |
| **4** | Kimball marts | 🏠 | dbt: `fct_trips`, `fct_station_availability`, conformed dims | BI-ready presentation layer | ⚪ |
| **5** | Data quality | 🏠 | Soda + dbt tests (freshness, uniqueness, bounds, row counts) | trust + a real QA gate | ⚪ |
| **6** | Orchestration | 🏠 | Airflow 3 cadence DAGs (daily feed / monthly trips), decoupled + re-runnable | automation + the DAG story | ⚪ |
| **7** | Showcase / BI | 🏠 | Evidence.dev dashboard on Gold + screenshots in README | the money-shot | ⚪ |
| **8** | Monitoring + chaos | 🏠 | Grafana freshness/SLA + alerts; chaos injector (drift/dupes/late/spikes) + incident log | ops maturity + prod-hardening | ⚪ |
| **9** | Cloud promotion | ☁️ | Terraform: MinIO→S3, catalog→Glue, DuckDB→Snowflake/BigQuery/Redshift on the same Iceberg; teardown | "same code, real cloud, many engines" | ⚪ |
| 10 | *(optional)* CD deploy | ☁️ | Deploy the stack to a VPS with health checks + rollback | "I can run it in prod" | ⚪ |

## Definition of done (per phase)
- Runs from a **single documented command**.
- Ships a **`LEARNING.md`** (annotated walkthrough — what & why).
- Has **tests** appropriate to the layer (pytest / dbt / Soda).
- **CI green**; docs updated; ADRs added if a real decision was made.
- Built on a **branch → PR → CI → merge** (never big work straight to `main`).

## Sequencing rule
We do **not** touch `cloud/` (Phase 9) until Phases 0–8 run end-to-end locally. Cloud is an overlay,
proven against a finished local pipeline — not built in parallel.
