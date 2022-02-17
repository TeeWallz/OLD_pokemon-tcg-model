select
	DISTINCT(data ->> 'artist') as artist
FROM {{ source('landing_tcgapi', 'ext_card') }}
