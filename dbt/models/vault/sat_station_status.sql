-- sat_station_status — high-frequency availability history for a station (change-detected).
-- This is where the GBFS snapshots become HISTORY the live feed never keeps.
{{ config(materialized='incremental', incremental_strategy='append') }}

{{ load_satellite(
    ref('stg_gbfs__station_status'),
    'station_hk',
    'status_hashdiff',
    ['num_bikes_available', 'num_docks_available', 'num_ebikes_available',
     'is_renting', 'is_returning', 'last_reported']
) }}
