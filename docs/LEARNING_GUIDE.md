# Learning guide

> **Purpose:** this repo is built to be *understood and explained*, not just to run. The goal: by the
> end, be able to explain **every tool, layer, and decision at a senior / interview level.** Learning is
> part of development, not an afterthought.

## How learning is embedded
1. **Per-phase `LEARNING.md`** — each phase folder ships an annotated walkthrough: what each tool/
   command/concept does, **why** it's there, the **alternatives**, and the **tradeoffs**. Written *as*
   the code is built.
2. **ADRs** ([`02-decisions.md`](02-decisions.md)) — every real decision with its "why not X". These are
   your ready-made answers to "why did you choose …?".
3. **Glossary** ([`GLOSSARY.md`](GLOSSARY.md)) — the vocabulary, in plain language, so you can *speak* it.
4. **This guide** — the index + the senior talking-points that grow each phase.

## The senior test (per concept)
For anything in this repo, you should be able to answer, unprompted:
- **What** is it and what problem does it solve?
- **Why** this and not the obvious alternative? (name the alternative + the tradeoff)
- **What breaks** if it's wrong, and how would you detect it?

## Per-phase LEARNING.md index
| Phase | Walkthrough | Key concepts you'll be able to explain |
|---|---|---|
| 1 · Ingestion | [`../ingestion/LEARNING.md`](../ingestion/LEARNING.md) | GBFS snapshots, immutable Bronze, idempotency, retry/backoff, why land raw |
| 2 · Lakehouse | [`../lakehouse/LEARNING.md`](../lakehouse/LEARNING.md) | Iceberg tables, catalogs (REST/Glue), snapshots & time-travel, hidden partitioning, schema evolution |
| 3 · Data Vault | _(added in phase)_ | hubs/links/satellites, hash keys, hashdiff, why append-only |
| 4 · Kimball | _(added in phase)_ | facts vs. dimensions, grain, SCD2, star vs. snowflake |
| 5 · Data quality | _(added in phase)_ | freshness/SLA, test severity, contracts |
| 6 · Orchestration | _(added in phase)_ | DAGs, cadence, idempotent tasks, backfill |
| 7 · Showcase | _(added in phase)_ | serving marts to BI, the "so what" |
| 8 · Monitoring + chaos | _(added in phase)_ | observability from output, schema drift, incident response |
| 9 · Cloud | _(added in phase)_ | portability, Iceberg across engines, FinOps |

## Senior talking-points (grows per phase)
> The 90-second version + the deep-dives. Fill in as phases ship; by the end this is your interview script.
- **Elevator pitch:** a local-first, $0 open lakehouse for real bike-share data — Data Vault 2.0 → Kimball,
  portable to Snowflake/BigQuery/Redshift by swapping one endpoint.
- **Hardest decision:** one Data Vault, not three (ADR-006) — hash divergence, cost, DV philosophy.
- _(more added per phase: the resilience story, the schema-drift incident, the freshness SLA, …)_
