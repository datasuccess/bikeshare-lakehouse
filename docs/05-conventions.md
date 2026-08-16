# 05 · Conventions

> **Purpose:** the rules that keep the repo legible and provenance-aware. The headline rule: **every
> file explains why it exists.**

## File-header convention (every source file)
Every code file (`.py`, `.sql`, `.yml` config, Dockerfile, etc.) starts with a header:

```python
# ── ingestion/gbfs_client.py ─────────────────────────────
# Purpose : fetch GBFS station feeds and land raw JSON in Bronze
# Why     : GBFS only serves "now"; we snapshot it to build history (ADR-008)
# Inputs  : GBFS feed URLs (env)      Outputs: bronze/gbfs/*.json on MinIO
# Adapted : resilience pattern inspired by cmc-crypto repo; rewritten for GBFS
# Docs    : docs/01-architecture.md · docs/03-data-model.md
```

- **Purpose** — one line: what this file does.
- **Why** — the reason it exists / the decision behind it (link the ADR).
- **Inputs → Outputs** — what it reads and produces.
- **Adapted** — *only if* a pattern was borrowed from another repo: cite it and say what changed.
  Never copy-paste a black box.
- **Docs** — the relevant docs for context.

**Markdown files** start with a one-line `> **Purpose:** …` blockquote instead of the code header.

## dbt naming
| Layer | Prefix | Example |
|---|---|---|
| staging | `stg_` | `stg_gbfs__station_status` |
| vault hub | `hub_` | `hub_station` |
| vault link | `lnk_` | `lnk_trip` |
| vault satellite | `sat_` | `sat_station_status` |
| dimension | `dim_` | `dim_station` |
| fact | `fct_` | `fct_trips` |

- One staging model per source object; `ref()` / `source()` always; **contracts on marts**; every
  model + column documented in schema YAML.

## Git & commits
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `test:`.
- **Branch → PR → CI → merge.** Never big work straight to `main`.
- **No AI co-authorship trailers.** Commits are authored solely by the repo owner.
- Secrets **never** committed — `.env` git-ignored, `.env.example` documents the keys, gitleaks in CI.

## Per-phase deliverables
Every phase folder ships a **`LEARNING.md`** — an annotated walkthrough explaining each tool, command,
and concept (e.g. *what a hashdiff is and why satellites use it*). Code is commented for a learner.

## Tooling
- Python 3.12 + **uv** (commit `uv.lock`); **Makefile** targets; **pre-commit** (ruff, sqlfluff,
  gitleaks, hygiene); **SQLFluff** (dialect=duckdb, templater=dbt).
- CI (GitHub Actions): secret-scan + hygiene now; grows into `dbt build` + tests on DuckDB once Phase 1
  lands.
