-- hub_station — the distinct list of station business keys (from GBFS *and* trips), append-only.
-- A hub holds only: the hash key, the business key, and when/where we first saw it.
{{ config(materialized='incremental', incremental_strategy='append') }}

with keys as (
    select station_hk, station_id, load_datetime, record_source
    from {{ ref('stg_gbfs__station_status') }}
    union all
    select station_hk, station_id, load_datetime, record_source
    from {{ ref('stg_gbfs__station_information') }}
    union all
    select start_station_hk, start_station_id, load_datetime, 'trips.start_station'
    from {{ ref('stg_trips') }}
    union all
    select end_station_hk, end_station_id, load_datetime, 'trips.end_station'
    from {{ ref('stg_trips') }}
),

ranked as (
    select
        station_hk,
        station_id,
        load_datetime,
        record_source,
        row_number() over (partition by station_hk order by load_datetime) as rn
    from keys
    where station_id is not null and trim(station_id) <> ''
)

select station_hk, station_id, load_datetime, record_source
from ranked
where rn = 1
{% if is_incremental() %}
    and station_hk not in (select station_hk from {{ this }})
{% endif %}
