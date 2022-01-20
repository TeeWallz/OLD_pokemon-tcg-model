{% macro set_create() %}

    {{ log("Creating set ddl...", info=true) }}
    
    {% set sql %}

        CREATE TABLE IF NOT EXISTS `set` (
            `id` varchar(20) PRIMARY KEY,
            `series` varchar(20),
            `printedTotal` int,
            `total` int,
            `ptcgoCode` varchar(255),
            `releaseDate` date,
            `updatedAt` datetime
        );

    {% endset %}

    {% do run_query(sql) %}
    
{% endmacro %}