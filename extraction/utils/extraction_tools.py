import requests, zipfile, io, os, json
import json
# import logging
import os
import pathlib
import urllib
from datetime import datetime, date
from pathlib import Path
import simplejson as simplejson
from sortedcontainers import SortedSet
from sqlalchemy import and_
from tqdm import tqdm
import time

from . import classes
from .sql_data_classes import *

# logger = logging.getLogger("Yeet")
# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] {%(pathname)s:%(lineno)d}\t%(levelname)s - \t%(message)s',
#     datefmt='%H:%M:%S'
# )

# todo: bulk inserts for cards section rather than adding individuallyr

debug_inserts = False


def clear_database():
    print("Wiping and refreshing database")
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(engine)


def refresh_api_extract(destination=None):
    if destination is None:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        destination = os.path.join(script_dir, "../data/external_staging/")

    zip_file_url = 'https://github.com/PokemonTCG/pokemon-tcg-data/archive/refs/heads/master.zip'
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(destination)


def readDataIntoSql():
    local_cache_data_dir = "/home/tom/git/home/pokemon-tcg-model/data/external_staging/"

    print("Loading data from tcg api into database")
    set_path = os.path.join(local_cache_data_dir, "pokemon-tcg-data-master/sets")

    raw_data = {
        'cards': {},
        'sets': {},
        'decks': {},
    }

    for set_language_file in os.listdir(set_path):
        langauge_code = set_language_file.replace(".json", "")
        set_language_file = os.path.join(set_path, set_language_file)

        with open(set_language_file) as set_language_downloaded_data:
            set_raw_dict = json.load(set_language_downloaded_data)
            for raw_set in set_raw_dict:
                raw_set['language'] = langauge_code
                raw_set['cards'] = []
                raw_set['decks'] = []
                raw_data['sets'][raw_set['id']] = raw_set

        for object_type in ('cards', 'decks'):
            object_dir = os.path.join(local_cache_data_dir, "pokemon-tcg-data-master", object_type)
            object_dict = raw_data[object_type]

            # For each language directory
            for language in os.listdir(object_dir):
                language_dir = os.path.join(object_dir, language)

                # For each file in language directory
                for object_filename in os.listdir(language_dir):
                    object_filename_full = os.path.join(language_dir, object_filename)
                    set_code = object_filename.replace('.json', '')

                    with open(object_filename_full) as object_f:
                        object_data = json.load(object_f)
                        for single_object in object_data:
                            if 'id' in single_object:
                                single_object['language'] = language
                                single_object['set'] = set_code
                                # Save the object into it'sown dictionary via reference
                                raw_data[object_type][single_object['id']] = single_object
                                # Append the ca4d to the set object
                                raw_data['sets'][set_code][object_type].append(single_object)
                            else:
                                print(
                                    f"\t\tSkipping load of tcg data api {object_type}/{set_code}/{single_object['name']} due to having no unique ID from the tcg api.")
    # destination.drop_and_reflect_database()

    # Single loops method. Set used to make sure that we only push unique values
    concepts_to_save = ["series", "languages", "legalities", "energys", "rarities",
                        "supertypes", "Artist", "setImageTypes", "cardImageTypes",
                        "cardJunctionsCreated",
                        "cardAbilitiesCreated", "cardAttacksCreated", "tcgSet", "SetLegality", "Cards",
                        "SetLocalisation", "SetImage", "CardLocalisation", "CardImage",
                        "CardAbility", "CardAbilityLocalisation", "CardAttack",
                        "CardAttackCost", "CardAttackLocalisation", "CardAttackLocalisation",
                        "CardNationalPokedexNumbers", "CardEnergyType", "CardLegalityOverride",
                        "CardEvolution", "CardRetreatCost", "CardWeakness"
                        ]
    concepts = {concept: set() for concept in concepts_to_save}

    print("Loading Basic objects")
    # Get Basic Objects
    for tcg_set in raw_data['sets'].values():
        concepts['series'].add(Series(tcg_set['series']))
        concepts['languages'].add(Language(tcg_set['language']))
        concepts['legalities'].update([Legality(legality) for legality in tcg_set['legalities'].keys()])
        concepts['setImageTypes'].update([SetImageType(image_type) for image_type in tcg_set['images'].keys()])

    for tcg_card in raw_data['cards'].values():
        concepts['supertypes'].add(SuperType(tcg_card['supertype']))
        concepts['cardImageTypes'].update([SetImageType(image_type) for image_type in tcg_card['images'].keys()])

        if 'artist' in tcg_card.keys():
            concepts['Artist'].add(Artist(tcg_card['artist'].replace(u'\xa0', u' ')))
        if 'rarity' in tcg_card:
            concepts['rarities'].add(Rarity(tcg_card['rarity']))
        # Energy
        if 'types' in tcg_card.keys():
            concepts['energys'].update([SetImageType(type) for type in tcg_card['types']])
        if 'attacks' in tcg_card.keys():
            for attack in tcg_card['attacks']:
                concepts['energys'].update([SetImageType(type) for type in attack['cost']])

    # Session.bulk_save_objects(list(concepts['Artist']))
    # Session.commit()
    # return

    # Debug loop to see which insert has an issue
    if debug_inserts:
        for serie in concepts['series']:
            Session.add(Series(serie))
        for language in concepts['languages']:
            Session.add(Language(language))
        for legality in concepts['legalities']:
            Session.add(Legality(legality))
        for energy in concepts['energys']:
            Session.add(EnergyType(energy))
        for rarity in concepts['rarities']:
            Session.add(Rarity(rarity))
        for supertype in concepts['supertypes']:
            Session.add(SuperType(supertype))
        time.sleep(2)
        for artist in concepts['artists']:
            print(f"Inserting {artist}")
            Session.add(Artist(artist))
            # Session.commit()
        for setImageType in concepts['setImageTypes']:
            Session.add(SetImageType(setImageType))
        for cardImageType in concepts['cardImageTypes']:
            Session.add(CardImageType(cardImageType))



    print("Loading Sets")
    # Get Sets
    for tcg_set in raw_data['sets'].values():
        concepts['tcgSet'].add(TCGSet({
            'id': tcg_set['id'],
            'series': tcg_set['series'],
            'printedTotal': tcg_set['printedTotal'],
            'total': tcg_set['total'],
            'ptcgoCode': tcg_set.get("ptcgoCode"),
            'releaseDate': datetime.strptime(tcg_set['releaseDate'], "%Y/%m/%d"),
            'updatedAt': datetime.strptime(tcg_set['updatedAt'], "%Y/%m/%d %H:%M:%S")
        }))

        concepts['SetLegality'].update(
            SetLegality(tcg_set.get('id'), set_legality) for set_legality in tcg_set['legalities'])

    # Session.commit()

    print("Loading Cards")
    # Get Cards
    session_cards = []
    session_new_set_localisation = []

    for tcg_card in raw_data['cards'].values():
        concepts['Cards'].add(
            Card({field: tcg_card.get(field) for field in ["id", 'set', 'number', 'hp', 'artist', 'supertype', 'rarity']})
        )
    #  {
    # Session.commit()

    print("Loading set localisations and images")
    # Get set localisation
    for tcg_set in raw_data['sets'].values():
        concepts['SetLocalisation'].add(SetLocalisation({
            'language': tcg_set.get('language'),
            'set': tcg_set.get('id'),
            'name': tcg_set.get('name')
        }))

        # SetImage
        for (imageType, imageUrl) in tcg_set.get("images").items():
            concepts['SetImage'].add(SetImage({
                'set': tcg_set.get('id'),
                'imageType': imageType,
                'language': tcg_set.get("language"),
                'url': imageUrl
            }))

    print("Loading card localisations and junctions")
    # Get card localisation and junctions
    # Session.commit()
    from time import sleep


    cards = raw_data['cards'].values()
    for i, tcg_card in enumerate(tqdm(cards)):
        # Junctions with languages, load every time
        concepts['CardLocalisation'].add(CardLocalisation({
            "card": tcg_card.get('id'),
            "language": tcg_card.get('language'),
            "name": tcg_card.get('name'),
            "flavor_text": tcg_card.get('flavourText')
        }))

        # CardImage
        for (imageType, imageUrl) in tcg_card.get("images").items():
            concepts['CardImage'].add(CardImage({
                "card": tcg_card.get('id'),
                "imageType": tcg_set.get("language"),
                "language": imageType,
                "url": imageUrl
            }))

        # CardAbility
        if 'abilities' in tcg_card.keys():
            for idx, ability in enumerate(tcg_card.get("abilities")):
                ability_key = "{}/{}".format(tcg_card.get('id'), idx)

                # Does the base ability exist? Only do this once
                concepts['CardAbility'].add(CardAbility({
                    "card": tcg_card.get('id'),
                    "index": idx,
                    "convertedEnergyCost": ability.get('convertedEnergyCost'),
                    "abilityType": ability.get('type'),
                }))

                # CardAbilityLocalisation, every time we see a card
                concepts['CardAbilityLocalisation'].add(CardAbilityLocalisation({
                    "card": tcg_card['id'],
                    "ability_index": idx,
                    "language": tcg_card['language'],
                    "text": ability['text']
                }))



        if 'attacks' in tcg_card.keys():
            for idx, attack in enumerate(tcg_card.get("attacks")):
                attack_key = "{}/{}".format(tcg_card.get('id'), idx)

                # Does the base ability exist? Only do this once
                # if attack_key not in cardAttacksCreated:
                concepts['CardAttack'].add(CardAttack({
                    "card": tcg_card.get('id'),
                    "index": idx,
                    "damage": attack.get('damage'),
                    "convertedEnergyCost": attack.get('convertedEnergyCost')
                }))

                # CardAttackCost
                if 'cost' in attack.keys():
                    for energy in set(attack['cost']):
                        concepts['CardAttackCost'].add(CardAttackCost({
                            "card": tcg_card.get('id'),
                            "attack_index": idx,
                            "energy_type": energy,
                            "amount": attack['cost'].count(energy)
                        }))

                # CardAttackLocalisation, run every time
                concepts["CardAttackLocalisation"].add(CardAttackLocalisation({
                    "language": tcg_card['language'],
                    "card": tcg_card.get('id'),
                    "attack_index": idx,
                    "text": attack['text']
                }))

        # Have we loaded junctions before? These are language independent so we only want to load them once
        # if tcg_card['id'] in cardJunctionsCreated:
        #     continue
        # cardJunctionsCreated.add(tcg_card['id'])

        if 'nationalPokedexNumbers' in tcg_card.keys():
            for nationalPokedexNumber in tcg_card['nationalPokedexNumbers']:
                concepts['CardNationalPokedexNumbers'].add(CardNationalPokedexNumbers({
                    "card": tcg_card.get('id'),
                    "nationalPokedexNumber": nationalPokedexNumber
                }))


        # CardEnergyType
        if 'types' in tcg_card.keys():
            for type in tcg_card['types']:
                concepts['CardEnergyType'].add(
                    CardEnergyType({
                        "card": tcg_card.get('id'),
                        "energy": type
                    })
                )

        # CardLegalityOverride
        # If there are specific legalities for a card that aren't in the set
        # Such as a banned card in a legal set
        card_legalities = tcg_card.get('legalities').keys()
        set_legalities = raw_data['sets'][tcg_card['set']]['legalities'].keys()
        if card_legalities != set_legalities:
            for card_legality in card_legalities:
                concepts['CardLegalityOverride'].add(CardLegalityOverride({
                    "card": tcg_card.get('id'),
                    "legality": card_legality
                }))

        # CardEvolution
        if 'evolvesTo' in tcg_card.keys():
            for evolution in tcg_card.get("evolvesTo"):
                concepts['CardEvolution'].add(CardEvolution({
                    "card": tcg_card.get('id'),
                    "pokemonName": evolution
                }))

        # CardRetreatCost
        if 'retreatCost' in tcg_card.keys():
            for energy in set(tcg_card['retreatCost']):
                concepts['CardRetreatCost'].add(CardRetreatCost({
                    "card": tcg_card.get('id'),
                    "energy_type": energy,
                    "amount": tcg_card['retreatCost'].count(energy)
                }))

        # weaknesses
        if 'weaknesses' in tcg_card.keys():
            for weakness in tcg_card.get('weaknesses'):
                # if tcg_card.get('id') == 'dp5-100':
                concepts['CardWeakness'].add(CardWeakness({
                    "card": tcg_card.get('id'),
                    "energy_type": weakness['type'],
                    "value": weakness['value']
                }))

    print("Comitting to database")

    for concept_key, concept_value in concepts.items():
        print(concept_key)
        Session.bulk_save_objects(list(concept_value))
        Session.commit()


    print("Saving JSON to database done.")


def save_database_to_json(self, source, destination_dir):
    pathlib.Path(destination_dir).mkdir(parents=True, exist_ok=True)

    sets_dir = os.path.join(destination_dir, 'sets')
    pathlib.Path(sets_dir).mkdir(parents=True, exist_ok=True)

    # For each language
    langs = source.session.query(Language).filter().all()
    sets = source.session.query(Set).filter().order_by(Set.releaseDate, Set.id).all()

    for lang in langs:
        language = lang.code
        sets_dict = []

        set_language_file = os.path.join(sets_dir, f"{language}.json")

        for set in sets:
            set_localisation = source.session.query(SetLocalisation).filter(
                and_(SetLocalisation.language == language, SetLocalisation.set == set.id)
            ).all()[0]
            set_legalities = source.session.query(SetLegality).filter(
                SetLegality.set == set.id
            ).all()
            set_images = source.session.query(SetImage).filter(
                SetImage.set == set.id
            ).all()

            new_set_dict = {}
            new_set_dict['id'] = set.id
            new_set_dict['name'] = set_localisation.name
            new_set_dict['series'] = set.series
            new_set_dict['printedTotal'] = set.printedTotal
            new_set_dict['total'] = set.total
            new_set_dict['legalities'] = {set_legality.legality: "Legal" for set_legality in set_legalities}
            if set.ptcgoCode is not None:
                new_set_dict['ptcgoCode'] = set.ptcgoCode
            new_set_dict['releaseDate'] = set.releaseDate.strftime("%Y/%m/%d")
            new_set_dict['updatedAt'] = set.updatedAt.strftime("%Y/%m/%d %H:%M:%S")
            new_set_dict['images'] = {set_image.imageType: set_image.url for set_image in set_images}

            sets_dict.append(new_set_dict)

        with open(set_language_file, "w") as f:
            f.write(simplejson.dumps(sets_dict, indent=2))

        kek = 1

    pass


def compare_data_directories(self, dir1, dir2):
    # Compare sets
    for filename in os.listdir(os.path.join(dir1, 'sets')):
        files = (
            os.path.join(dir1, 'sets', filename),
            os.path.join(dir2, 'sets', filename),
        )
        kek = ordered(json.load(open(files[0]))) == ordered(json.load(open(files[1])))
        heh = 2
    pass


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


if __name__ == "__main__":
    # refresh_api_extract()
    clear_database()
    readDataIntoSql()
    pass
