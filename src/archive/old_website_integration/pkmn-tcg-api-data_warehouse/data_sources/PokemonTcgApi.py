import json
import logging
import os
import pathlib
import urllib
from datetime import datetime, date
from pathlib import Path

import simplejson as simplejson
from sortedcontainers import SortedSet
from sqlalchemy import and_

from data_sources.data_source import DataSource
# from database_objects.tcg_data import *

logging.basicConfig(
     level=logging.DEBUG,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d}\t%(levelname)s - \t%(message)s',
     datefmt='%H:%M:%S'
 )

# logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
logger = logging.getLogger(__name__)


class PokemonTcgApi(DataSource):
    source_url = "https://github.com/PokemonTCG/pokemon-tcg-data/archive/refs/heads/master.zip"
    local_cache_name = "PokemonTcgApi"

    def load_data(self):
        logger.info("Loading data from tcg api into class PokemonTcgApi")
        set_path = os.path.join(self.local_cache_data_dir, "pokemon-tcg-data-master/sets")

        self.raw_data = {
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
                    self.raw_data['sets'][raw_set['id']] = raw_set

            for object_type in ('cards', 'decks'):
                object_dir = os.path.join(self.local_cache_data_dir, "pokemon-tcg-data-master", object_type)
                object_dict = self.raw_data[object_type]

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
                                    self.raw_data[object_type][single_object['id']] = single_object
                                    # Append the ca4d to the set object
                                    self.raw_data['sets'][set_code][object_type].append(single_object)
                                else:
                                    logger.info(
                                        f"\t\tSkipping load of tcg data api {object_type}/{set_code}/{single_object['name']} due to having no unique ID from the tcg api.")

    def replicate_data(self, destination):
        logger.info("Replicating data from PokemonTcgApi BEGIN")

        destination.drop_and_reflect_database()

        # Single loops method
        series = set()
        languages = set()
        legalities = set()
        energys = set()
        rarities = set()
        supertypes = set()
        artists = set()

        setImageTypes = set()
        cardImageTypes = set()

        setsCreated = set()
        cardsCreated = set()
        cardJunctionsCreated = set()
        cardAbilitiesCreated = set()
        cardAttacksCreated = set()


        logger.info("Loading Basic objects")
        # Get Basic Objects
        for tcg_set in self.raw_data['sets'].values():
            series.add(tcg_set['series'])
            languages.add(tcg_set['language'])
            legalities.update(tcg_set['legalities'].keys())
            setImageTypes.update(tcg_set['images'].keys())

        for tcg_card in self.raw_data['cards'].values():
            supertypes.add(tcg_card['supertype'])
            cardImageTypes.update(tcg_card['images'].keys())

            if 'artist' in tcg_card.keys():
                artists.add(tcg_card['artist'].replace(u'\xa0', u' '))

            if 'rarity' in tcg_card:
                rarities.add(tcg_card['rarity'])

            #Energy
            if 'types' in tcg_card.keys():
                energys.update(tcg_card['types'])
            if 'attacks' in tcg_card.keys():
                for attack in tcg_card['attacks']:
                    energys.update(attack['cost'])

        for serie in series:
            destination.session.add(Series(serie))
        for language in languages:
            destination.session.add(Language(language))
        for legality in legalities:
            destination.session.add(Legality(legality))
        for energy in energys:
            destination.session.add(EnergyType(energy))
        for rarity in rarities:
            destination.session.add(Rarity(rarity))
        for supertype in supertypes:
            destination.session.add(SuperType(supertype))
        for artist in artists:
            try:
                destination.session.add(Artist(artist))
                #destination.session.commit()
            except Exception as ex:
                kek = 1
        for setImageType in setImageTypes:
            destination.session.add(SetImageType(setImageType))
        for cardImageType in cardImageTypes:
            destination.session.add(CardImageType(cardImageType))

        #destination.session.commit()

        logger.info("Loading Sets")
        # Get Sets
        for tcg_set in self.raw_data['sets'].values():
            if tcg_set['id'] in setsCreated:
                continue
            setsCreated.add(tcg_set['id'])

            new_set = Set()
            new_set.id = tcg_set['id']
            new_set.series = tcg_set['series']
            new_set.printedTotal = tcg_set['printedTotal']
            new_set.total = tcg_set['total']
            if 'ptcgoCode' in tcg_set.keys():
                new_set.ptcgoCode = tcg_set['ptcgoCode']
            new_set.releaseDate = datetime.strptime(tcg_set['releaseDate'], "%Y/%m/%d")
            new_set.updatedAt = datetime.strptime(tcg_set['updatedAt'], "%Y/%m/%d %H:%M:%S")
            destination.session.add(new_set)

            for set_legality in tcg_set['legalities']:
                new_setlegality = SetLegality()
                new_setlegality.set = tcg_set.get('id')
                new_setlegality.legality = set_legality
                destination.session.add(new_setlegality)

        destination.session.commit()

        logger.info("Loading Cards")
        #Get Cards
        for tcg_card in self.raw_data['cards'].values():
            if tcg_card['id'] in cardsCreated:
                continue
            cardsCreated.add(tcg_card['id'])

            new_card = Card()
            new_card.id = tcg_card['id']
            new_card.set = tcg_card['set']
            new_card.number = tcg_card['number']
            if 'hp' in tcg_card.keys():
                new_card.hp = tcg_card['hp']
            new_card.supertype = tcg_card['supertype']
            if 'artist' in tcg_card.keys():
                new_card.artist = tcg_card['artist']
            if 'rarity' in tcg_card.keys():
                new_card.rarity = tcg_card['rarity']
            destination.session.add(new_card)
        destination.session.commit()

        logger.info("Loading set localisations and images")
        # Get set localisation
        for tcg_set in self.raw_data['sets'].values():
            new_set_localisation = SetLocalisation()
            new_set_localisation.language = tcg_set.get('language')
            new_set_localisation.set = tcg_set.get('id')
            new_set_localisation.name = tcg_set.get('name')
            destination.session.add(new_set_localisation)

            #SetImage
            for (imageType, imageUrl) in tcg_set.get("images").items():
                new_set_image = SetImage()
                new_set_image.set = tcg_set.get('id')
                new_set_image.language = tcg_set.get("language")
                new_set_image.imageType = imageType
                new_set_image.url = imageUrl
                destination.session.add(new_set_image)

        logger.info("Loading card localisations and junctions")
        # Get card localisation and junctions
        destination.session.commit()
        from time import sleep
        from tqdm import tqdm

        cards = self.raw_data['cards'].values()
        for i, tcg_card in enumerate(tqdm(cards)):
            # Junctions with languages, load every time
            new_card_localisation = CardLocalisation()
            new_card_localisation.card = tcg_card.get('id')
            new_card_localisation.language = tcg_card.get('language')
            new_card_localisation.name = tcg_card.get('name')
            new_card_localisation.flavor_text = tcg_card.get('flavourText')
            destination.session.add(new_card_localisation)

            #CardImage
            for (imageType, imageUrl) in tcg_card.get("images").items():
                new_card_image = CardImage()
                new_card_image.card = tcg_card.get('id')
                new_card_image.language = tcg_set.get("language")
                new_card_image.imageType = imageType
                new_card_image.url = imageUrl
                destination.session.add(new_card_image)


            # CardAbility
            if 'abilities' in tcg_card.keys():
                for idx, ability in enumerate(tcg_card.get("abilities")):
                    ability_key = "{}/{}".format(tcg_card.get('id'), idx)

                    # Does the base ability exist? Only do this once
                    if ability_key not in cardAbilitiesCreated:
                        new_ability = CardAbility()
                        new_ability.card = tcg_card.get('id')
                        new_ability.index = idx
                        if 'convertedEnergyCost' in ability.keys():
                            new_ability.convertedEnergyCost = ability['convertedEnergyCost']
                        if 'type' in ability.keys():
                            new_ability.abilityType = ability['type']
                        destination.session.add(new_ability)

                        cardAbilitiesCreated.add(ability_key)

                    # CardAbilityLocalisation, every time we see a card
                    new_cardabilitylocalisation = CardAbilityLocalisation()
                    new_cardabilitylocalisation.language = tcg_card['language']
                    new_cardabilitylocalisation.card = tcg_card['id']
                    new_cardabilitylocalisation.ability_index = idx
                    new_cardabilitylocalisation.text = ability['text']
                    destination.session.add(new_cardabilitylocalisation)

            if 'attacks' in tcg_card.keys():
                for idx, attack in enumerate(tcg_card.get("attacks")):
                    attack_key = "{}/{}".format(tcg_card.get('id'), idx)

                    # Does the base ability exist? Only do this once
                    if attack_key not in cardAttacksCreated:
                        new_attack = CardAttack()
                        new_attack.card = tcg_card.get('id')
                        new_attack.index = idx
                        new_attack.damage = attack.get('damage')
                        new_attack.convertedEnergyCost = attack.get('convertedEnergyCost')
                        destination.session.add(new_attack)
                        #destination.session.commit()

                        # CardAttackCost
                        if 'cost' in attack.keys():
                            for energy in set(attack['cost']):
                                new_CardAttackCost = CardAttackCost()
                                new_CardAttackCost.card = tcg_card.get('id')
                                new_CardAttackCost.attack_index = idx
                                new_CardAttackCost.energy_type = energy
                                new_CardAttackCost.amount = attack['cost'].count(energy)
                                destination.session.add(new_CardAttackCost)

                        cardAttacksCreated.add(attack_key)

                    # CardAttackLocalisation, run every time
                    new_cardAttackLocalisation = CardAttackLocalisation()
                    new_cardAttackLocalisation.language = tcg_card['language']
                    new_cardAttackLocalisation.card = tcg_card.get('id')
                    new_cardAttackLocalisation.attack_index = idx
                    new_cardAttackLocalisation.text = attack['text']
                    destination.session.add(new_cardAttackLocalisation)
                    # destination.session.commit()



            # Have we loaded junctions before? These are language independent so we only want to load them once
            if tcg_card['id'] in cardJunctionsCreated:
                continue
            cardJunctionsCreated.add(tcg_card['id'])

            if 'nationalPokedexNumbers' in tcg_card.keys():
                for dexNo in tcg_card['nationalPokedexNumbers']:
                    new_CardNationalPokedexNumbers = CardNationalPokedexNumbers()
                    new_CardNationalPokedexNumbers.card = tcg_card.get('id')
                    new_CardNationalPokedexNumbers.nationalPokedexNumber = dexNo
                    destination.session.add(new_CardNationalPokedexNumbers)
                    #destination.session.commit()

            #CardEnergyType
            if 'types' in tcg_card.keys():
                for type in tcg_card['types']:
                    new_card_type = CardEnergyType()
                    new_card_type.card = tcg_card.get('id')
                    new_card_type.energy = type
                    destination.session.add(new_card_type)

            #CardLegalityOverride
            card_legalities = tcg_card.get('legalities').keys()
            set_legalities = self.raw_data['sets'][tcg_card['set']]['legalities'].keys()
            if card_legalities != set_legalities:
                for card_legality in card_legalities:
                    new_card_legality = CardLegalityOverride()
                    new_card_legality.card = tcg_card.get('id')
                    new_card_legality.legality = card_legality
                    destination.session.add(new_card_legality)


            #CardEvolution
            if 'evolvesTo' in tcg_card.keys():
                for evolution in tcg_card.get("evolvesTo"):
                    new_card_evolution = CardEvolution()
                    new_card_evolution.card = tcg_card.get('id')
                    new_card_evolution.pokemonName = evolution
                    destination.session.add(new_card_evolution)

            #CardRetreatCost
            if 'retreatCost' in tcg_card.keys():
                for energy in set(tcg_card['retreatCost']):
                    new_CardRetreatCost = CardRetreatCost()
                    new_CardRetreatCost.card = tcg_card.get('id')
                    new_CardRetreatCost.energy_type = energy
                    new_CardRetreatCost.amount = tcg_card['retreatCost'].count(energy)
                    destination.session.add(new_CardRetreatCost)

            #weaknesses
            if 'weaknesses' in tcg_card.keys():
                for weakness in tcg_card.get('weaknesses'):
                    # if tcg_card.get('id') == 'dp5-100':
                    new_CardWeakness = CardWeakness()
                    new_CardWeakness.card = tcg_card.get('id')
                    new_CardWeakness.energy_type = weakness['type']
                    new_CardWeakness.value = weakness['value']
                    destination.session.add(new_CardWeakness)

            destination.session.commit()



        logger.info("Replicating data from PokemonTcgApi DONE")

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
                    and_(SetLocalisation.language==language, SetLocalisation.set == set.id)
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
                new_set_dict['legalities'] = {set_legality.legality:"Legal" for set_legality in set_legalities}
                if set.ptcgoCode is not None:
                    new_set_dict['ptcgoCode'] = set.ptcgoCode
                new_set_dict['releaseDate'] = set.releaseDate.strftime("%Y/%m/%d")
                new_set_dict['updatedAt'] = set.updatedAt.strftime("%Y/%m/%d %H:%M:%S")
                new_set_dict['images'] = {set_image.imageType:set_image.url for set_image in set_images}

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

if __name__ == '__main__':
    result = PokemonTcgApi()
    breakpoint_line = 1
