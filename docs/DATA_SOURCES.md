# Data sources, licensing & attribution

> **Purpose:** document every external data source, its license, and required attribution. Respecting
> open-data license terms is a governance basic that most portfolios skip — this one doesn't.

## Sources
| Source | What | Access | License / terms |
|---|---|---|---|
| **GBFS feed** | Real-time station information & status (and free-bike status where published) | Public HTTP, **no key** | Per-system license via the operator's **GBFS `system_information`** / license URL — recorded per system before ingestion |
| **Historical trip files** | Monthly trip records (start/end station, time, bike, member type) | Public download, **no key** | The operator's **open-data license agreement** (e.g. system-specific "data license agreement") |

> The exact system (e.g. Capital Bikeshare / Citi Bike / a European operator) is chosen at the start of
> Phase 1; this file is then filled with that system's **feed URLs, license name, license URL, and the
> attribution string** their terms require.

## Attribution
- Attribution text mandated by the chosen system's license will be reproduced here **and** surfaced in
  the showcase dashboard footer.

## Privacy
- Sources are **station- and trip-level**; **no personal data** is ingested or stored. Some operators
  bucket/round trip timestamps or drop rider identifiers precisely to prevent re-identification — we
  keep only those already-anonymized fields. See [`../SECURITY.md`](../SECURITY.md).

## Compliance rules
- Honor each source's **rate limits** and **caching/refresh guidance** (GBFS publishes a `ttl`).
- Never redistribute raw source data beyond what the license permits; this repo commits **no data** at all.
