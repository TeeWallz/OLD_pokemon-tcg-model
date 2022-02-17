select
	DISTINCT(data ->> 'superype') as superype
FROM {{ source('landing_tcgapi', 'ext_card') }}
