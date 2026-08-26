{# load_satellite — the Data Vault satellite load pattern (append-only, change-detected).
   For each parent key, keep a row only when the hashdiff CHANGES vs the previous reading (ordered by
   load_datetime). Unchanged consecutive readings are dropped, so a satellite stores *history*, not
   duplicates. Incremental runs only process load_datetimes newer than what's already stored.
   Note (teaching): this dedups within the incoming batch; a production sat also compares the first
   new row to the current stored latest (datavault4dbt does this) — a refinement we call out in LEARNING. #}
{% macro load_satellite(staging_relation, parent_hk, hashdiff, payload_cols) %}
with staged as (
    select
        {{ parent_hk }},
        {{ hashdiff }},
        load_datetime,
        record_source,
        {{ payload_cols | join(",\n        ") }}
    from {{ staging_relation }}
    {% if is_incremental() %}
    where load_datetime > (select max(load_datetime) from {{ this }})
    {% endif %}
),

flagged as (
    select
        *,
        lag({{ hashdiff }}) over (partition by {{ parent_hk }} order by load_datetime) as _prev_hashdiff
    from staged
)

select
    {{ parent_hk }},
    {{ hashdiff }},
    load_datetime,
    record_source,
    {{ payload_cols | join(",\n    ") }}
from flagged
where _prev_hashdiff is null or {{ hashdiff }} != _prev_hashdiff
{% endmacro %}
