
SELECT
	id,
	name,
	series,
	printedTotal,
	total,
	legalities,
	legality_unlimited,
	legality_standard,
	legality_expanded,
	ptcgoCode,
	releaseDate,
	updatedAt,
	images_symbol,
	images_logo
FROM {{ ref('vw_set') }}