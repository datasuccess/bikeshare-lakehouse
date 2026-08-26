-- stg_trips — clean historical trips + add DV hashes.
-- A trip is an EVENT connecting two stations, so it becomes a transactional LINK keyed by ride_id
-- (the data has no bike id). Feeds hub_station (start/end), lnk_trip, sat_trip_details.
with src as (
    select * from {{ source('bronze', 'raw_trips') }}
)

select
    {{ dv_hash(['ride_id']) }} as trip_hk,
    {{ dv_hash(['start_station_id']) }} as start_station_hk,
    {{ dv_hash(['end_station_id']) }} as end_station_hk,
    {{ dv_hash(['rideable_type', 'member_casual', 'started_at', 'ended_at']) }} as trip_hashdiff,
    ride_id,
    rideable_type,
    member_casual,
    start_station_id,
    end_station_id,
    start_station_name,
    end_station_name,
    started_at,
    ended_at,
    strptime(ym || '01', '%Y%m%d') as load_datetime,
    'trips' as record_source
from src
