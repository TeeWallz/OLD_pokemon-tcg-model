select
	set_id,
	id AS card_id
FROM
    {{ ref('vw_card') }}

