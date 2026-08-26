-- sat_trip_details — attributes of a trip (the link's descriptive data).
-- Trips are immutable, so in practice one row per ride_id; modelled as a satellite for consistency.
{{ config(materialized='incremental', incremental_strategy='append') }}

{{ load_satellite(
    ref('stg_trips'),
    'trip_hk',
    'trip_hashdiff',
    ['rideable_type', 'member_casual', 'started_at', 'ended_at',
     'start_station_name', 'end_station_name']
) }}
