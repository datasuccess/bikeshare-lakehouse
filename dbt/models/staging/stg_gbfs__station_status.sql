-- stg_gbfs__station_status — clean the raw status readings + add DV hash key/hashdiff.
-- Grain: one row per station per snapshot. Feeds hub_station + sat_station_status.
with src as (
    select * from {{ source('bronze', 'raw_station_status') }}
)

select
    {{ dv_hash(['station_id']) }} as station_hk,
    {{ dv_hash([
        'num_bikes_available', 'num_docks_available', 'num_ebikes_available',
        'is_renting', 'is_returning'
    ]) }} as status_hashdiff,
    station_id,
    num_bikes_available,
    num_docks_available,
    num_ebikes_available,
    is_renting,
    is_returning,
    last_reported,
    to_timestamp(snapshot_ts) as load_datetime,
    'gbfs.station_status' as record_source
from src
