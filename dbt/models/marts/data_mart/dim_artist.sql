select
	DISTINCT artist
FROM {{ ref('vw_card') }}
