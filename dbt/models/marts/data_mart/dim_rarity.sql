select
	DISTINCT rarity
FROM {{ ref('vw_card') }}
