{% macro set_legality_create() %}
    
    {{ log("Creating set_legality ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `set_legality` (
            `set` varchar(20),
            `legality` varchar(255),
            PRIMARY KEY (`set`, `legality`)
        );


    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}