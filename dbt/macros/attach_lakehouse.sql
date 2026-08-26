{# attach_lakehouse — attach the Iceberg REST catalog as `lake` (run via on-run-start).
   Why: makes lake.bronze.raw_* queryable. AUTHORIZATION_TYPE 'none' because the local
   fixture is open; the cloud catalog (Glue) swaps this for real auth. #}
{% macro attach_lakehouse() %}
    ATTACH IF NOT EXISTS '' AS lake (
        TYPE iceberg,
        ENDPOINT '{{ env_var("CATALOG_URI", "http://localhost:8181") }}',
        AUTHORIZATION_TYPE 'none'
    )
{% endmacro %}
