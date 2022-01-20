{% macro set_images_create() %}
    
    {{ log("Creating set_images ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `set_images` (
            `set` varchar(20),
            `type` varchar(255),
            `url` varchar(255),
            PRIMARY KEY (`set`, `type`)
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}