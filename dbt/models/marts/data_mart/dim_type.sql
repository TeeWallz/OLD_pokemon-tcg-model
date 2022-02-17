select
	distinct json_array_elements_text(types) as types
FROM
	{{ ref('vw_card') }}
