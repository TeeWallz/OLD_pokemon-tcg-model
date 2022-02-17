with variations as (
	select
		vw_card.id,
		set_id,
		number_int,
		json_object_keys(vw_card.tcgplayer -> 'prices') as variation
	from {{ ref('vw_card') }}
)
select
	id,
	set_id,
    number_int,
	variation
from 
	variations
where variation not like '1st%'
ORDER by
	set_id,
	number_int,
	array_position(array['unlimited', 'normal','holofoil', 'unlimitedHolofoil', 'reverseHolofoil'], variation)
