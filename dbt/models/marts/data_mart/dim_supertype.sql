select
	DISTINCT supertype
FROM {{ ref('vw_card') }}
