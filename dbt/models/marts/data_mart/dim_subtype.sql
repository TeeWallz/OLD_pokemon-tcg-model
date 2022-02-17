select
	distinct json_array_elements_text(subtypes) as subtypes
from
	{{ ref('vw_card') }}