{% macro language_create() %}
    
    {{ log("Creating language ddl...", info=true) }}

    {% set sql %}

        CREATE TABLE IF NOT EXISTS `language` (
            `code` varchar(20) PRIMARY KEY,
            `name` varchar(50)
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}