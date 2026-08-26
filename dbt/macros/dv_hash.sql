{# dv_hash — Data Vault 2.0 hash of one or more columns.
   Why: DV joins on a deterministic md5(business_key) surrogate, not the natural key — stable keys,
   parallel loads, and a fixed-width join column. We standardize (trim + upper + cast) and delimit
   with '||' so 'a','b' can never collide with 'ab'. Used for BOTH hub/link keys and satellite
   hashdiffs (a hashdiff is just a hash over the descriptive columns). #}
{% macro dv_hash(columns) %}
    md5(
        {%- for col in columns %}
        coalesce(trim(upper(cast({{ col }} as varchar))), ''){% if not loop.last %} || '||' || {% endif %}
        {%- endfor %}
    )
{% endmacro %}
