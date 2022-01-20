{% macro create_ddl() %}
    
    {% do series_create() %}
    {% do language_create() %}
    {% do set_create() %}
    {% do set_name_create() %}
    {% do set_hpcode_create() %}
    {% do legality_create() %}
    {% do set_legality_create() %}
    {% do energy_type_create() %}
    {% do rarity_create() %}
    {% do card_create() %}
    
    
{% endmacro %}