# COST — the money model

> **Purpose:** be explicit about cost at every stage. Local is $0; the cloud phase is opt-in, trial-
> /free-tier-first, and always ships a teardown. FinOps awareness is a deliberate signal.

## Local track (Phases 0–8): **$0**
Everything runs in Docker on a laptop. No accounts, no keys, no bill:
- **MinIO** (local S3), **Postgres**, **Airflow**, **DuckDB**, **dbt**, **Soda**, **Grafana**,
  **Evidence.dev** — all open-source, all containerized.
- Public data sources (GBFS + trip files) are free and keyless.

## Cloud track (Phase 9): opt-in, trial/free-tier first
Populated when Phase 9 is built. Target: **near-$0 at synthetic scale**, with hard teardown.

| Service | Free/trial reality (small scale) | Teardown |
|---|---|---|
| **AWS S3 + Glue** | pennies at GB scale | `terraform destroy` |
| **Snowflake** | ~$400 trial credits | drop objects / let trial lapse |
| **BigQuery** | 1 TB/mo query + 10 GB storage **free** | `terraform destroy` |
| **Redshift** | Serverless trial credits | `terraform destroy` |

## Rules (ADR-001, ADR-006)
- **Nothing cloud runs by default.** The default `make` targets are 100% local.
- Every cloud resource is **Terraform-managed** and has a documented `destroy`.
- Prefer **OIDC / short-lived creds**; never commit long-lived keys.
- Data volume is kept **small on purpose** (bump only for a "full-looking" dashboard demo).

*(Real per-run $ estimates get filled in as Phase 9 is built.)*
