# cloud/ — opt-in cloud overlay (LATER)

> **Purpose:** promote the finished local pipeline to real cloud **without changing the pipeline code**
> — just the storage endpoint and dbt target. **Status:** intentionally empty until Phases 0–8 run
> end-to-end locally (ADR-010).

## What will live here (Phase 9)
- `terraform/` — IaC for **AWS S3** (Iceberg warehouse) + **Glue** (catalog) + warehouse resources,
  each with a documented `terraform destroy`.
- `profiles/` — dbt targets for **Snowflake / BigQuery / Redshift**, all reading the **same Gold Iceberg**.
- `docs/` — promotion runbook + `COST.md` updates + teardown.

## The rule
This directory does **not** get built early and does **not** fork the pipeline. Local is the source of
truth; cloud is the same code with `AWS_ENDPOINT_URL` + `dbt --target` swapped. The **Data Vault is
built once**; only the Kimball marts are served to the three engines (ADR-006).

Empty for now, on purpose.
