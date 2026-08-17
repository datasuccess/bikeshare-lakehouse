# Data sources, licensing & attribution

> **Purpose:** document every external data source, its license, and required attribution. Respecting
> open-data license terms is a governance basic most portfolios skip — this one doesn't.

## System: Capital Bikeshare (Washington, D.C.) — `dca-cabi`
Operated by Lyft. Chosen for a clean GBFS feed + a long, well-structured historical trip archive under
a clear open-data license (ADR-008).

## Sources
| Source | What | Access | Notes |
|---|---|---|---|
| **GBFS discovery** | auto-discovery of all feed URLs | `https://gbfs.capitalbikeshare.com/gbfs/gbfs.json` | **GBFS v1.1**; multi-language (en/fr/es) |
| **`station_information`** | station id, name, lat/lon, capacity | `https://gbfs.lyft.com/gbfs/1.1/dca-cabi/en/station_information.json` | slowly-changing → `sat_station_info` |
| **`station_status`** | bikes/docks available, is_renting | `https://gbfs.lyft.com/gbfs/1.1/dca-cabi/en/station_status.json` | **ttl 60s**; snapshot → `sat_station_status` |
| **Historical trips** | monthly trip records (ZIP of CSV) | `https://s3.amazonaws.com/capitalbikeshare-data/` | file pattern `YYYYMM-capitalbikeshare-tripdata.zip` |

> Always resolve live feed URLs from the **discovery** document rather than hard-coding — the URLs above
> are the current values and may change. The code discovers them at runtime.

## Trip-file schema (note the real schema drift)
Capital Bikeshare changed its trip schema — a genuine, documented evolution we exploit in the Phase 8
schema-drift drill:
- **Current (2020-05 →):** `ride_id, rideable_type, started_at, ended_at, start_station_name,
  start_station_id, end_station_name, end_station_id, start_lat, start_lng, end_lat, end_lng, member_casual`
- **Legacy (→ 2020-04):** `Duration, Start date, End date, Start station number, Start station,
  End station number, End station, Bike number, Member type`

Phase 1 targets the **current** schema. Note: staff trips, test-station trips, and rides < 60s are
already removed by the provider.

## License & attribution
- **License:** *Capital Bikeshare Data License Agreement* (see the provider's system-data page).
- **Attribution:** the license's required attribution string will be reproduced here **and** in the
  showcase dashboard footer once the dashboard exists (Phase 7).

## Privacy
- Data is **station- and trip-level**; **no PII**. The provider already anonymizes (no rider IDs; short
  trips removed). We keep only these already-anonymized fields. See [`../SECURITY.md`](../SECURITY.md).

## Compliance rules
- Honor GBFS **`ttl`** (60s) — don't poll faster than the feed refreshes.
- This repo commits **no source data** at all (`.gitignore` excludes the lake); we only redistribute
  derived, aggregated results as permitted.
