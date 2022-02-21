select
	set_id,
    rarity,
	supertype,
	max(releasedate) as releasedate,
	variation_list,
	string_agg(
		id,
		','
		ORDER BY number_int
	) as card_list,
	count(*) as variation_count
from 
	{{ ref('stg_tp_card_variations_agg') }}
group by set_id, rarity, supertype, variation_list
order by
	releasedate, set_id, rarity, supertype
