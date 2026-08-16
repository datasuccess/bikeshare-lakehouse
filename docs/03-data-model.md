# 03 · Data model

> **Purpose:** define the sources and the two-layer model — **Data Vault 2.0** (Silver, integration)
> and **Kimball** (Gold, presentation) — for the bike-share domain. This is the modelling spec the dbt
> project (Phases 3–4) will implement.

## Sources (real, public, no key)
| Source | Cadence | Shape | Feeds |
|---|---|---|---|
| **GBFS `station_information`** | on change (daily pull) | station name, capacity, lat/lon | `hub_station`, `sat_station_info` (SCD) |
| **GBFS `station_status`** | high (e.g. every N min / hourly) | bikes & docks available, is_renting | `sat_station_status` (time-series) |
| **GBFS `free_bike_status`** *(if published)* | high | free-floating bike location/status | `hub_bike`, `sat_bike_status` |
| **Historical trip files** (monthly CSV) | monthly (batch) | start/end station, time, bike, member type | `link_trip`, `sat_trip_details` |

> GBFS serves only the **current** snapshot. Capturing snapshots over time to build history is exactly
> what the satellites do — the core Data Vault story here.

## Silver — Data Vault 2.0
**Hubs** (a business key + its hash):
- `hub_station` — bk: `station_id` (+ `system_id`)
- `hub_bike` — bk: `bike_id`
- `hub_system` — bk: `system_id` (the city/operator)

**Links** (relationships between hubs):
- `link_trip` — `hub_bike` × start `hub_station` × end `hub_station` (a completed trip)
- `link_station_system` — `hub_station` × `hub_system`

**Satellites** (descriptive attributes + change history via `hashdiff`):
- `sat_station_info` — name, capacity, lat/lon, region (**slowly changing**)
- `sat_station_status` — num_bikes_available, num_docks_available, is_renting (**high-frequency**)
- `sat_bike_status` — bike state/location over time
- `sat_trip_details` — duration, member_type, distance (attributes of `link_trip`)

**DV2.0 mechanics** (applied uniformly):
- **Hash keys** on business keys; **hashdiff** on satellite payloads to detect change.
- **Append-only**, with `load_datetime` + `record_source`; **idempotent** loads (re-running a batch is a no-op).
- Business keys standardized before hashing (trim/upper) to keep hashes stable.

## Gold — Kimball star
**Dimensions:**
- `dim_station` (SCD2 from `sat_station_info`) — name, capacity, location, system
- `dim_date` / `dim_time` — calendar + time-of-day
- `dim_bike` — bike attributes
- `dim_member_type` — casual / member

**Facts:**
- `fct_trips` — grain: **one row per trip**. Measures: duration, distance; FKs: start/end station, bike, date, member type.
- `fct_station_availability` — grain: **one row per station per status snapshot**. Measures: bikes/docks available, utilization %.

## Medallion ↔ layer mapping
```
Bronze (raw JSON/CSV)  ──►  Silver = Data Vault 2.0 (hubs/links/sats, Iceberg)  ──►  Gold = Kimball (facts/dims, Iceberg)
```

## Example analytics the Gold layer answers
- Busiest stations & hours (rebalancing signal) · trip duration distribution by member type ·
  net flow per station (arrivals − departures) · availability / stock-out rate over time (SLA) ·
  seasonality of ridership.

*(Column-level detail lands with the dbt models in Phases 3–4; this doc is the blueprint they follow.)*
