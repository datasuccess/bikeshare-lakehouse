# 02 · Architecture Decision Records (ADRs)

> **Purpose:** record every load-bearing decision with its context and tradeoffs, so the "why" is
> never lost and a reviewer can see the judgment behind the build. Format is deliberately short.

Each ADR: **Decision · Why · Tradeoff / when I'd choose differently.**

---

### ADR-001 — Local-first, $0 by default
**Decision:** the entire platform runs on a laptop (Docker) before any cloud spend.
**Why:** fast iteration, no bill while the model is still moving, and anyone can reproduce it.
**Tradeoff:** local engines (DuckDB) aren't the cloud warehouses; parity is proven in Phase 9, not assumed.

### ADR-002 — MinIO + Iceberg for storage portability
**Decision:** land data as **Apache Iceberg** on **MinIO** locally.
**Why:** MinIO is S3-API-compatible and Iceberg is engine-portable, so local↔cloud is an endpoint swap,
not a rewrite. This is the backbone of the "two tracks, one codebase" design.
**Tradeoff:** Iceberg adds catalog/metadata machinery vs. plain Parquet; worth it for portability + time-travel.

### ADR-003 — DuckDB as the local query/transform engine
**Decision:** DuckDB runs dbt locally.
**Why:** single-node, file-based, zero-config, fast on "small data"; $0.
**Tradeoff:** not distributed; large-scale is a cloud-warehouse concern (Phase 9), not a local one.

### ADR-004 — Data Vault 2.0 as the Silver integration layer
**Decision:** model Silver as DV2.0 (hubs / links / satellites, hash keys, hashdiff, append-only).
**Why:** bike-share has stable business keys + high-frequency history — a textbook DV fit; gives an
auditable, source-agnostic system of record.
**Tradeoff:** more moving parts than a straight star. Justified here for the learning + history story.
DV runs on Iceberg/DuckDB by default; Postgres is the alt if a relational vault engine is wanted.

### ADR-005 — Kimball star as the Gold presentation layer
**Decision:** serve Gold as Kimball facts + conformed dimensions.
**Why:** BI-performant, intuitive for consumers, the industry default for marts.
**Tradeoff:** none material — it's the right tool for the serving layer.

### ADR-006 — Build the Data Vault **once**; serve Kimball to all three warehouses
**Decision:** the Data Vault is a single canonical build. In the cloud phase, Snowflake / BigQuery /
Redshift **read the same Gold Iceberg** (and/or materialize the Kimball marts natively) — we do **not**
build three independent vaults.
**Why:** DV is *by definition* the single integrated system of record. Building it 3× also causes
**hash-key divergence** (engines differ on concat/NULL/hash semantics), triples cost, and triples
dialect maintenance.
**Tradeoff:** slightly less "native warehouse depth" per engine — bought back by showing the modern
"one open dataset, many engines, zero lock-in" pattern, which is more senior.

### ADR-007 — Airflow 3 as the orchestrator
**Decision:** Airflow 3 (cadence-based DAGs), in Docker locally.
**Why:** most employable orchestrator; asset-aware scheduling in v3; matches real-world stacks.
**Tradeoff:** heavier than a cron/Makefile; Dagster was the main alternative (asset-native) — Airflow
chosen for employability + ecosystem.

### ADR-008 — Domain: public bike-share (GBFS live feed + historical trip files)
**Decision:** two free, no-key public sources — GBFS real-time station feed + monthly trip CSV dumps.
**Why:** GBFS gives a live snapshot feed (great DV satellite + freshness story); trip files give volume
+ a batch/backfill pattern. Two cadences, one coherent model. Deliberately **not crypto** (differentiates
from the repo this project was inspired by).
**Tradeoff:** GBFS only serves "now" — building history is *our* job (a feature, not a limitation).

### ADR-009 — Real API **and** a synthetic chaos injector
**Decision:** use the real API for the happy path; add a synthetic **chaos injector** for prod-issue drills.
**Why:** a live API can't be forced to produce schema drift, duplicates, late data, or volume spikes on
demand. The injector supplies exactly those, so we can *demonstrate* handling them. Best of both worlds.
**Tradeoff:** a little extra code to maintain; high payoff for the reliability story (see [`../chaos/`](../chaos/)).

### ADR-010 — One repo; cloud is an opt-in overlay, not a fork
**Decision:** local and cloud live in one repo; cloud code sits in [`../cloud/`](../cloud/), added only
after the local pipeline is complete.
**Why:** preserves the "same code, swap endpoint" story and avoids maintaining two ~80%-identical repos.
**Tradeoff:** the repo carries an (initially empty) cloud dir; a small price for one coherent narrative.

### ADR-011 — Education-first + a file-header convention
**Decision:** every phase ships a `LEARNING.md`; every source file starts with a purpose/why header.
**Why:** the repo is a teaching artifact as much as a pipeline; provenance and intent must be legible.
**Tradeoff:** more prose per file — intentional. Convention defined in [`05-conventions.md`](05-conventions.md).
