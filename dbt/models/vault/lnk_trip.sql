-- lnk_trip — a transactional link: one row per trip (ride_id) connecting start & end station hubs.
-- Trips are immutable events, so the link is append-only and never updated.
{{ config(materialized='incremental', incremental_strategy='append') }}

with staged as (
    select
        trip_hk,
        start_station_hk,
        end_station_hk,
        ride_id,
        load_datetime,
        record_source
    from {{ ref('stg_trips') }}
),

ranked as (
    select *, row_number() over (partition by trip_hk order by load_datetime) as rn
    from staged
)

select trip_hk, start_station_hk, end_station_hk, ride_id, load_datetime, record_source
from ranked
where rn = 1
{% if is_incremental() %}
    and trip_hk not in (select trip_hk from {{ this }})
{% endif %}
