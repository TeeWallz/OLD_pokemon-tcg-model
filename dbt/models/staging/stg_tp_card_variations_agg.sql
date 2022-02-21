select
	max(set_id) as set_id,
	max(id) as id,
	max(number_int) as number_int,
	max(rarity) as rarity,
	max(supertype) as supertype,
	max(releasedate) as releasedate,
	string_agg(
		variation,
		','
		ORDER BY array_position(array['unlimited', 'normal','holofoil', 'unlimitedHolofoil', 'reverseHolofoil'], variation)
		) as variation_list,
	count(*) as variation_count
from 
	{{ ref('stg_tp_card_variations') }}
group by id
order by set_id, number_int