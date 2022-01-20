{% macro legality_create() %}
    
{{ log("Creating legality ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `legality` (
            `name` varchar(255) PRIMARY KEY
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}