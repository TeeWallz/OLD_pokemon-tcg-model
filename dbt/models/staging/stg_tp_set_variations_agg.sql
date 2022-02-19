with set_rarity_variation_count as (
	select set_id, rarity, count(distinct variation_list) as variation_group_count from 
	{{ ref('stg_tp_card_variations_agg') }}
	group by  set_id, rarity
)
select
	stg_tp_card_variations_agg.set_id,
    stg_tp_card_variations_agg.rarity,
	max(releasedate) as releasedate,
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
group by stg_tp_card_variations_agg.set_id, stg_tp_card_variations_agg.rarity, variation_list
order by
	variation_group_count desc, releasedate desc, set_id