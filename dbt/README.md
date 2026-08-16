# dbt/ — the one transformation project

> **Purpose:** a single dbt project that builds **staging → Data Vault 2.0 → Kimball marts**, extended
> across phases. One project, many targets. **Status:** planned (Phases 3–4). Spec only.

## Planned layout
```
dbt/
├── dbt_project.yml
├── profiles.yml            targets: duckdb (local)  ·  snowflake / bigquery / redshift (cloud, later)
├── models/
│   ├── staging/            stg_gbfs__*  ·  stg_trips__*   (one per source object)
│   ├── vault/              hub_* · lnk_* · sat_*          (Data Vault 2.0, Silver)
│   └── marts/              dim_* · fct_*                  (Kimball, Gold)
└── tests/                  singular data-quality tests
```

## Principles (see docs/05-conventions.md)
- Naming: `stg_ / hub_ / lnk_ / sat_ / dim_ / fct_`.
- `ref()` / `source()` always; **contracts on marts**; every model + column documented.
- Vault built **once**; marts served to all engines (ADR-006). Hash keys + hashdiff in the vault layer.
- Default target = **DuckDB** (local, $0). Cloud targets added in Phase 9.

Model blueprint: [`../docs/03-data-model.md`](../docs/03-data-model.md).
