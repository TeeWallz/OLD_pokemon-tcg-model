{% macro set_hpcode_create() %}

    {{ log("Creating set_hpcode ddl...", info=true) }}
    
    {% set sql %}

        CREATE TABLE IF NOT EXISTS `set_hpcode` (
            `language` varchar(20),
            `set` varchar(20),
            `hp_code` varchar(100),
            PRIMARY KEY (`language`, `set`)
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}