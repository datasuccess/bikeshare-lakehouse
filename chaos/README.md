# chaos/ — synthetic prod-issue injector

> **Purpose:** deliberately create the failures a *live* API never will, so we can **demonstrate**
> handling them. This is the flexibility a real public API can't give (ADR-009).
> **Status:** planned (Phase 8). Spec only.

## Planned injections
- **Schema drift** — a renamed/added/removed field in a GBFS payload.
- **Duplicates** — replayed records with the same business key.
- **Late-arriving data** — a snapshot with an out-of-order `load_datetime`.
- **Volume spike** — 10× the normal batch size.
- **Source failure** — simulated HTTP 429 / 500 to exercise retry/backoff.

## Deliverable
Each drill is paired with an **incident-log entry**: what was injected → how monitoring/tests caught it
→ how the pipeline recovered. This becomes the reliability story in
[`../docs/CASE_STUDY.md`](../docs/CASE_STUDY.md).
