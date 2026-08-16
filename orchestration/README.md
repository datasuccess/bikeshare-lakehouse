# orchestration/ — Airflow 3 DAGs

> **Purpose:** schedule and connect the pipeline stages on cadence. **Status:** planned (Phase 6). Spec only.

## Planned contents
- `dags/gbfs_daily.py` — high-cadence: fetch GBFS → land Bronze → vault → marts → data-quality.
- `dags/trips_monthly.py` — monthly: download trip files → land → vault → marts → DQ.
- `dags/backfill.py` — parameterized backfill over a date range.

## Principles (patterns validated in the cmc-crypto reference repo, ADR-007)
- **Cadence-based** DAGs (daily feed vs monthly trips) to match how the data actually changes.
- **Decoupled, re-runnable stages** — each step independently retryable after failure.
- **Idempotent** tasks — safe to re-run; deterministic per-batch load windows.

Airflow runs in the local Docker stack ([`../infra/`](../infra/)).
