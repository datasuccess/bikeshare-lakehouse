# 01 · Architecture

> **Purpose:** the reference architecture — layers, data flow, how medallion maps to Data Vault, and
> the local→cloud portability principle that the whole project is built around.

## The portability principle (the core idea)
> **Local and cloud run the *same code* because MinIO speaks the S3 API and Iceberg is a portable
> table format.** Promotion changes only `AWS_ENDPOINT_URL` and the dbt `--target`.

This is why there is **one repo, not two**, and why cloud is an opt-in overlay rather than a fork.

## Layers (medallion)
```
Sources ──► Bronze (raw) ──► Silver (Data Vault 2.0) ──► Gold (Kimball) ──► BI / consumers
```

| Layer | Local storage | Format | Built by | Purpose |
|---|---|---|---|---|
| **Bronze** | MinIO `bronze/` | raw JSON / CSV | ingestion | immutable raw landing — replayable source of truth |
| **Silver** | MinIO `silver/` | **Iceberg** | dbt | **Data Vault 2.0** — integrated, auditable history |
| **Gold** | MinIO `gold/` | **Iceberg** | dbt | **Kimball** star schema — BI-performant marts |
| **Serve** | — | — | Evidence / warehouses | dashboards, ad-hoc SQL, cloud warehouses |

## Why medallion **and** Data Vault?
They answer different questions and compose cleanly:
- **Medallion** = *data quality zones* (raw → cleansed → curated). An operational convention.
- **Data Vault 2.0** = *how the Silver integration layer is modelled* (hubs/links/satellites, hash
  keys, append-only history). It is the auditable, source-agnostic system of record.
- **Kimball** = *how Gold is shaped for consumption* (facts + conformed dimensions).

So: **Silver *is* the Data Vault; Gold *is* Kimball.** Mapping detail in
[`03-data-model.md`](03-data-model.md).

## Data flow (local)
1. **Ingest** — Airflow triggers the GBFS loader (snapshots, high cadence) and the trip-file loader
   (monthly, batch). Raw payloads land in Bronze on MinIO, unchanged. *(Phase 1)*
2. **Vault** — dbt reads Bronze, hashes business keys, and loads hubs/links/satellites into Silver as
   Iceberg. Append-only; re-runs are idempotent. *(Phases 2–3)*
3. **Marts** — dbt builds Kimball facts + dimensions in Gold from the vault. *(Phase 4)*
4. **Validate** — Soda + dbt tests gate the run (freshness, uniqueness, bounds). *(Phase 5)*
5. **Serve** — Evidence.dev dashboard on Gold; Grafana watches feed freshness / SLA. *(Phases 7–8)*

Everything above is orchestrated by **Airflow 3** with cadence-based DAGs (see
[`../orchestration/`](../orchestration/)).

## Engines
- **DuckDB** — the local query/transform engine for dbt. Single-node, file-based, $0.
- **Postgres** — Airflow's metadata DB **and** the Data Vault engine when a warehouse-grade store is
  wanted locally (Iceberg-on-DuckDB is the default; Postgres is the alt — see ADR-004).
- **Cloud (later):** Snowflake/BigQuery/Redshift read the **same Gold Iceberg** on S3 (ADR-006).

## Local → cloud (the overlay, added in Phase 9)
```
MinIO   → AWS S3        (endpoint swap; ingestion code unchanged)
local   → AWS Glue      (Iceberg REST catalog)
DuckDB  → Snowflake / BigQuery / Redshift   (dbt --target; same Gold Iceberg)
compose → Terraform     (IaC, with `terraform destroy` teardown)
```
The **Data Vault is still built once**; only the Kimball marts are served to the three warehouses.
Rationale (hash divergence, cost, DV philosophy) in ADR-006.

## Diagrams
Rendered versions of the above (hero, medallion, DAG graph, star schema, dbt lineage) live in
[`diagrams/`](diagrams/) and are embedded in the top-level `README.md`.
