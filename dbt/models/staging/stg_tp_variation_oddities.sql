select * from 
{{ ref('stg_tp_set_variations_agg') }}
where variation_group_count > 1