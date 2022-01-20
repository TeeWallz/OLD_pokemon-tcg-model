{% macro energy_type_create() %}
    
    {{ log("Creating energy_type ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `energy_type` (
            `name` varchar(255) PRIMARY KEY
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}