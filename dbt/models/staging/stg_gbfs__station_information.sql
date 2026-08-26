-- stg_gbfs__station_information — clean station attributes + add DV hash key/hashdiff.
-- Grain: one row per station per snapshot. Feeds hub_station + sat_station_info.
with src as (
    select * from {{ source('bronze', 'raw_station_information') }}
)

select
    {{ dv_hash(['station_id']) }} as station_hk,
    {{ dv_hash(['name', 'lat', 'lon', 'capacity', 'region_id']) }} as info_hashdiff,
    station_id,
    name,
    lat,
    lon,
    capacity,
    region_id,
    to_timestamp(snapshot_ts) as load_datetime,
    'gbfs.station_information' as record_source
from src
