-- sat_station_info — descriptive station attributes over time (SCD via hashdiff).
-- A new row only when name/lat/lon/capacity/region actually change.
{{ config(materialized='incremental', incremental_strategy='append') }}

{{ load_satellite(
    ref('stg_gbfs__station_information'),
    'station_hk',
    'info_hashdiff',
    ['station_id', 'name', 'lat', 'lon', 'capacity', 'region_id']
) }}
