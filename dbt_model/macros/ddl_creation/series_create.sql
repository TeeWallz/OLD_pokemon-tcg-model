{% macro series_create() %}

    {{ log("Creating series ddl...", info=true) }}
    
    {% set sql %}

        CREATE TABLE IF NOT EXISTS `series` (
        `name` varchar(50) PRIMARY KEY
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}