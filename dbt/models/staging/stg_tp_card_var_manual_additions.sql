select
    vw_card.set_id,
    card_variation_additions.card_id as id,
    vw_card.number_int,
    vw_card.rarity,
    vw_card.supertype,
    vw_set.releasedate,
    card_variation_additions.variation
from {{ ref('card_variation_additions') }}
left join {{ ref('vw_card') }}
    on card_variation_additions.card_id = vw_card.id
left join {{ ref('vw_set') }}
    on vw_card.set_id = vw_set.id