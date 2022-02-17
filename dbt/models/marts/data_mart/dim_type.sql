select
	distinct json_array_elements_text(data -> 'types') as types
FROM
	{{ source('landing_tcgapi', 'ext_card') }}
