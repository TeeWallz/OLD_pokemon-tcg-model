select
	DISTINCT(data ->> 'rarity') as rarity
FROM {{ source('landing_tcgapi', 'ext_card') }}
