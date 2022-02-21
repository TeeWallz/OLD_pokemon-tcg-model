with set_rarity_variation_count as (
	select set_id, rarity, supertype, count(distinct variation_list) as variation_group_count from 
	{{ ref('stg_tp_card_variations_agg') }}
	group by  set_id, rarity, supertype
)
select
	stg_tp_card_variations_agg.set_id,
	max(releasedate) as releasedate,
    stg_tp_card_variations_agg.rarity,
	stg_tp_card_variations_agg.supertype,
	variation_list,
	max(variation_group_count) as variation_group_count,
	count(*) as variation_count,
		string_agg(
		id,
		','
		ORDER BY number_int
	) as card_list
from 
	{{ ref('stg_tp_card_variations_agg') }}
	left join
	set_rarity_variation_count
		on stg_tp_card_variations_agg.set_id = set_rarity_variation_count.set_id
		and stg_tp_card_variations_agg.rarity = set_rarity_variation_count.rarity
		and stg_tp_card_variations_agg.supertype = set_rarity_variation_count.supertype
		
group by
	stg_tp_card_variations_agg.set_id,
	stg_tp_card_variations_agg.rarity,
	stg_tp_card_variations_agg.supertype,
	variation_list
order by
	variation_group_count desc, releasedate desc, set_id