{% macro card_create() %}
    
    {{ log("Creating card ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `card` (
            `id` varchar(255) PRIMARY KEY,
            `set` varchar(20),
            `number` varchar(255),
            `name` varchar(255),
            `hp` varchar(255),
            `supertype` varchar(255),
            `artist` varchar(255),
            `rarity` varchar(255)
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}