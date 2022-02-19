with variations as (
	select
		set_id,
		vw_card.id,
		vw_card.rarity,
		vw_set.releasedate,
		number_int,
		json_object_keys(vw_card.tcgplayer -> 'prices') as variation
	from {{ ref('vw_card') }}
	left join {{ ref('vw_set') }}
		on vw_card.set_id = vw_set.id
)
select
	set_id,
	id,
	number_int,
	rarity,
	releasedate,
	variation
from 
	variations
where variation not like '1st%'
ORDER by
	releasedate,
	number_int,
	array_position(array['unlimited', 'normal','holofoil', 'unlimitedHolofoil', 'reverseHolofoil'], variation)
