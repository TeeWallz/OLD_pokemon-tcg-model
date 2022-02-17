select
	rarity
FROM {{ ref('vw_card') }}
