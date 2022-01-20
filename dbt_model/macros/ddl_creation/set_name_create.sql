{% macro set_name_create() %}
    
    {{ log("Creating set_name ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `set_name` (
            `language` varchar(20),
            `set` varchar(20),
            `name` varchar(100),
            PRIMARY KEY (`language`, `set`)
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}