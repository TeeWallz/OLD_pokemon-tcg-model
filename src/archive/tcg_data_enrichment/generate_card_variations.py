import csv
from typing import List, Set
import requests, json
from dataclasses import dataclass, field
import sqlite3
from tqdm import tqdm
from .sql_utils import init_sql
from pokemontcgsdk import Set as Tcg_Set, Card, RestClient

# The ultinate goal is to pull all variations of a card and generate a unique SKU number for the price
# Questions:
#    For each set, what are the possible variations for a single card
#          i.e. Normal & Reverse, Normal, Holo, Holo & Reverse
#          Thi is to get a state of play for variations and see if there are any wierdness

sets_url = "https://api.pokemontcg.io/v2/sets?orderby=releaseDate"
tcg_sets = Tcg_Set.all()
variations = set()
variation_tbl_name = "variations"
RestClient.configure('4440c304-d5c0-4939-b533-5befa084795c')

def load_card_variations(conn_string):
    variations = []
    sql_interface = init_sql(conn_string)

    try:
        sql_interface.models.CardVariations.__table__.drop()
    except Exception:
        pass
    sql_interface.Base.metadata.create_all()

    sets_to_load = [x for x in tcg_sets if x.releaseDate > '2010/01/01']

    for tcg_set in (pbar := tqdm(tqdm(sets_to_load), position=0, leave=True)):
        description = f"Processing {tcg_set.name}"
        pbar.set_description(description, refresh=True)
        cards = Card.where(q=f"set.id:{tcg_set.id}")

        for card in cards:
            if card.tcgplayer is None:
                variations.append(sql_interface.models.CardVariations(card.id, None))
            elif card.tcgplayer.prices is None:
                variations.append(sql_interface.models.CardVariations(card.id, None))
            else:
                if card.tcgplayer.prices.holofoil is not None:
                    variations.append(sql_interface.models.CardVariations(card.id, 'holofoil', card.tcgplayer.prices.holofoil.market))
                if card.tcgplayer.prices.normal is not None:
                    variations.append(sql_interface.models.CardVariations(card.id, 'normal', card.tcgplayer.prices.normal.market))
                if card.tcgplayer.prices.reverseHolofoil is not None:
                    variations.append(sql_interface.models.CardVariations(card.id, 'reverseHolofoil', card.tcgplayer.prices.reverseHolofoil.market))


    sql_interface.Session.bulk_save_objects(variations)
    sql_interface.Session.commit()

kek = 1
#
# variations_sorted = list(variations)
# variations_sorted.sort()
#
# #from another class
# with open("/home/tom/git/home/pokemon-tcg-model/curacards/data/set_variations.csv", 'w') as csv_file:
#     writer = csv.writer(csv_file, delimiter=',')
#
#     writer.writerow(['set', 'rarity', 'variation', 'suffix'])
#     for variation in variations_sorted:
#         row = variation.csv_row()
#
#
#         writer.writerow(list(row))  # @Shankar suggestion






