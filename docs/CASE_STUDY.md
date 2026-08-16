# Case study — bikeshare-lakehouse

> **Purpose:** the narrative a reviewer reads in ~90 seconds — problem → architecture → one hard
> decision → result. This is a **skeleton**; sections fill in as phases ship. Lead with judgment, not
> a tool list.

## Problem
Public bike-share systems expose a **live GBFS feed** that only ever shows *"now"* — no history — plus
**monthly trip dumps**. Turning that into trustworthy analytics (busiest stations, rebalancing signals,
availability SLAs) needs a pipeline that **captures history**, integrates two very different cadences,
and stays reproducible and cheap.

## Architecture (one paragraph + the hero diagram)
Open lakehouse: raw → **Data Vault 2.0** (Silver) → **Kimball** (Gold), as Iceberg on MinIO, queried by
DuckDB, orchestrated by Airflow 3 — **all local at $0**, and **portable to Snowflake/BigQuery/Redshift**
by swapping one endpoint. *(embed `docs/diagrams/hero.svg`)*

## The hard decision (deep-dive) — *one vault, not three*
When the plan called for Snowflake **and** BigQuery **and** Redshift, the tempting move was to build the
whole Data Vault in each. I didn't — because a Data Vault is *by definition* the single integrated
system of record, and building it three times causes **hash-key divergence** across engines, triples
cost, and triples maintenance. Instead: **build the vault once, serve the Kimball marts to all three**
from the same Gold Iceberg. That's the modern "one open dataset, many engines, zero lock-in" pattern.
*(See ADR-006.)*

## Results *(fill in as built)*
- _e.g._ N stations, M trips, X snapshots of history captured; dashboard link; freshness SLA met %; CI runtime.

## What I'd do differently *(fill in)*
- Honest reflections — a real limitation, a tradeoff I'd revisit, the next thing I'd build (streaming/CDC?).

## Links
- Live dashboard · dbt docs/lineage · repo · LinkedIn writeup *(added as they exist)*
