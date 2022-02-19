with base as (
	select distinct set_id, vw_set.releasedate, variation_list
    from
        {{ ref('stg_tcgplayer_card_variations_agg') }}
	left join {{ ref('vw_set') }}
		on set_id = vw_set.id
	order by  vw_set.releasedate, variation_list
)
select
	base.set_id,
	base.variation_list,
	COUNT(*) as count,
	MAX(vw_set.total) as total,
	COUNT(*) / MAX(vw_set.total::float) as proportion
from
	base
left join 
	{{ ref('vw_set') }}
	on
		base.set_id = vw_set.id
left join 
	{{ ref('stg_tcgplayer_card_variations_agg') }}
	on stg_tcgplayer_variations_agg.set_id = base.set_id
	and stg_tcgplayer_variations_agg.variation_list = base.variation_list
group by base.set_id, base.variation_list
