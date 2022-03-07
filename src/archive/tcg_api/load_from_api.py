import json
from tqdm import tqdm

from tcg_api.querybuilder import QueryBuilder
from tcg_api.database_orm import ORM_Class

def load(connection_string):
    print("Connecting to database...")
    db = ORM_Class(connection_string, reset_database=True)
    print("Connecting to database done.")

    print("Loading sets into db...")
    QueryBuilder('ext_sets').all(db, load_into_database)
    print("Loading sets into db done.")

    print("Downloading cards from API...")
    cards = QueryBuilder('ext_cards').all(db, load_into_database)
    print("Downloading cards from API done.")

    print("Loading cards into db...")
    for card in (pbar := tqdm(tqdm(cards), position=0, leave=True)):
        pbar.set_description(cards['set']['id'], refresh=True)

        card_orm = db.models.Card(id=card['id'], json=json.dumps(card))
        db.Session.add(card_orm)
        db.Session.commit()
    print("Loading cards into db done.")

    jej = 1

def load_into_database(db, objects, name):
    for object in objects:
        orm = db.models[name](id=object['id'], json=json.dumps(object))
        db.Session.add(orm)
    db.Session.commit()