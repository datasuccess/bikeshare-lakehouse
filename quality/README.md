# quality/ — data quality checks

> **Purpose:** gate the pipeline on trust — nothing reaches Gold that fails validation.
> **Status:** planned (Phase 5). Spec only.

## Planned contents
- `soda/checks/` — declarative YAML checks: **freshness** (feed ≤ N min old), **uniqueness** (station
  keys), **not-null**, **row-count** deltas, **sanity bounds** (bikes_available ≥ 0 ≤ capacity).
- dbt tests — generic (`not_null`, `unique`, `relationships`, `accepted_range`) + singular DQ tests.

## Principles
- **Two layers of testing:** dbt tests inside the transform graph; Soda as an independent production QA
  gate run by Airflow after loads.
- Failures **store results** and **alert** (Phase 8), rather than silently passing.

See [`../docs/03-data-model.md`](../docs/03-data-model.md) for the entities being validated.
