{{ config(materialized='table') }}

select
	data ->> 'id' AS id,
	data ->> 'name' as name,
	data ->> 'series' as series,
	data ->> 'printedTotal' as printedTotal,
	data ->> 'total' as total,
	data -> 'legalities' as legalities,
	data -> 'legalities' ->> 'unlimited' as legality_unlimited,
	data -> 'legalities' ->> 'standard' as legality_standard,
	data -> 'legalities' ->> 'expanded' as legality_expanded,
	data ->> 'ptcgoCode' as ptcgoCode,
	TO_DATE(data ->> 'releaseDate', 'YYYY/MM/DD') as releaseDate,
	TO_TIMESTAMP(data ->> 'updatedAt', 'YYYY/MM/DD') as updatedAt,
	data -> 'images' ->> 'symbol' as images_symbol,
	data -> 'images' ->> 'logo' as images_logo
FROM {{ source('landing_tcgapi', 'ext_set') }}