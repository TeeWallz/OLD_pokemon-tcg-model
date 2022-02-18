select
	id,
	set_id,
	string_agg(variation, ',') as variation_list,
	count(*) as variation_count
from 
	{{ ref('stg_tcgplayer_card_variations') }}
group by id, number_int, set_id
order by set_id, number_int