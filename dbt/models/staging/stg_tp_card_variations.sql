with tcglayer_variations as (
	select
		vw_card.id,
		json_object_keys(vw_card.tcgplayer -> 'prices') as variation
	from {{ ref('vw_card') }}
),
base as (
	select
		tcglayer_variations.id,
		tcglayer_variations.variation
	from 
		tcglayer_variations
	LEFT JOIN  {{ ref('stg_tp_card_var_manual_removals') }}
		on tcglayer_variations.id = stg_tp_card_var_manual_removals.card_id
		and tcglayer_variations.variation = stg_tp_card_var_manual_removals.variation
	where tcglayer_variations.variation not like '1st%'
		AND stg_tp_card_var_manual_removals.card_id is null
	union
	SELECT
		id,
		variation
	FROM
		{{ ref('stg_tp_card_var_manual_additions') }}
)
SELECT
	vw_card.set_id,
	base.id,
	vw_card.number_int,
	vw_card.rarity,
	vw_card.supertype,
	vw_set.releasedate,
	base.variation
FROM base
	left join {{ ref('vw_card') }}
		on base.id = vw_card.id
	left join {{ ref('vw_set') }}
		on vw_card.set_id = vw_set.id
ORDER by
	releasedate,
	number_int,
	array_position(array['unlimited', 'normal','holofoil', 'unlimitedHolofoil', 'reverseHolofoil'], variation)
