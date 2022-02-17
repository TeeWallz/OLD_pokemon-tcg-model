select
    distinct json_object_keys(vw_card.tcgplayer -> 'prices') as variation
from
    {{ ref('vw_card') }}