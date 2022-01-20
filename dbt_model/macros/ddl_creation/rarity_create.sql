{% macro rarity_create() %}
    
    {{ log("Creating rarity ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `rarity` (
            `name` varchar(255) PRIMARY KEY
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}