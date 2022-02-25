select
    card_variation_removals.card_id,
    card_variation_removals.variation
from {{ ref('card_variation_removals') }}
-- left join {{ ref('vw_card') }}
--     on card_variation_additions.card_id = vw_card.id
-- left join {{ ref('vw_set') }}
--     on vw_card.set_id = vw_set.id