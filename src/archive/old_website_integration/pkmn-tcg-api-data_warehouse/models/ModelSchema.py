from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Date, DateTime, MetaData, \
    ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from models.base import Base

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d}\t%(levelname)s - \t%(message)s',
    datefmt='%H:%M:%S'
)


class TcgData:
    engine = None

    def __init__(self, engine_string):
        self.engine = create_engine(engine_string)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        # Base.query = self.session.query_property()

    def drop_and_reflect_database(self):
        logger.info("Wiping and refreshing database")
        Base.metadata.drop_all(bind=self.engine, checkfirst=True)
        Base.metadata.create_all(self.engine)



class ApiObject(Base):
    __abstract__ = True
    __tablename__ = "ApiObject"
    __table_args__ = {"schema": "tcg_data_new"}

# Parent Attributes / Enums
class Series(ApiObject):
    __tablename__ = "series"
    name = Column(String(50), primary_key=True)

    def __init__(self, name):
        self.name = name


class Language(ApiObject):
    __tablename__ = "language"
    code = Column(String(20), primary_key=True)
    name = Column(String(50))

    def __init__(self, code):
        self.code = code


class Legality(ApiObject):
    __tablename__ = "legality"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name




class Rarity(ApiObject):
    __tablename__ = "rarity"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name


class SuperType(ApiObject):
    __tablename__ = "supertype"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name


class Artist(ApiObject):
    __tablename__ = "artist"
    name = Column(String(50), primary_key=True)

    def __init__(self, name):
        self.name = name


# Main Objects
class Set(ApiObject):
    __tablename__ = "set"
    id = Column(String(20), primary_key=True)
    series = Column(String(50), ForeignKey(Series.name))
    printedTotal = Column(Integer)
    total = Column(Integer)
    ptcgoCode = Column(String(20))
    releaseDate = Column(Date)
    updatedAt = Column(DateTime)


# Localization and many-to-many junctions
class SetLocalisation(ApiObject):
    __tablename__ = "set_localisation"
    language = Column(String(20), ForeignKey(Language.code), primary_key=True)
    set = Column(String(20), ForeignKey(Set.id), primary_key=True)
    name = Column(String(50))


class SetLegality(ApiObject):
    __tablename__ = "set_legality"
    set = Column(String(20), ForeignKey(Set.id), primary_key=True)
    legality = Column(String(20), ForeignKey(Legality.name), primary_key=True)


class SetImageType(ApiObject):
    __tablename__ = "set_image_type"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name


class SetImage(ApiObject):
    __tablename__ = "set_image"
    set = Column(String(20), ForeignKey(Set.id), primary_key=True)
    imageType = Column(String(20), ForeignKey(SetImageType.name), primary_key=True)
    language = Column(String(20), ForeignKey(Language.code), primary_key=True)
    url = Column(String(200))


# Card and constituent fields
class Card(ApiObject):
    __tablename__ = "card"
    id = Column(String(20), primary_key=True, comment="generated field from '{set}-{number}'")
    set = Column(String(20), ForeignKey(Set.id))
    number = Column(String(20))
    hp = Column(String(20))
    supertype = Column(String(20), ForeignKey(SuperType.name))
    rarity = Column(String(20), ForeignKey(Rarity.name))


# Localization and many-to-many junctions
class CardLocalisation(ApiObject):
    __tablename__ = "card_localisation"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    language = Column(String(20), ForeignKey(Language.code), primary_key=True)
    name = Column(String(100))
    flavor_text = Column(String(100))




class CardImageType(ApiObject):
    __tablename__ = "card_image_type"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name


class CardImage(ApiObject):
    __tablename__ = "card_image"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    imageType = Column(String(20), ForeignKey(CardImageType.name), primary_key=True)
    language = language = Column(String(20), ForeignKey(Language.code), primary_key=True)
    url = Column(String(200))


class CardLegalityOverride(ApiObject):
    __tablename__ = "card_legality_override"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    legality = Column(String(20), ForeignKey(Legality.name), primary_key=True)


class CardEvolution(ApiObject):
    __tablename__ = "card_evolution"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    pokemonName = Column(String(100), primary_key=True)
    nationalPokedexNumber = Column(String(5))

class CardAbility(ApiObject):
    __tablename__ = "card_ability"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    index = Column(Integer, primary_key=True, index=True)
    convertedEnergyCost = Column(Integer)
    abilityType = Column(String(20))


class CardAbilityLocalisation(ApiObject):
    __tablename__ = "card_ability_localisation"
    pk = Column(Integer, primary_key=True, autoincrement=True, default=0)
    card = Column(String(20), ForeignKey(CardAbility.card), index=True)
    ability_index = Column(Integer, ForeignKey(CardAbility.index), index=True)
    language = Column(String(20), ForeignKey(Language.code), index=True)
    text = Column(String(1000))
    __table_args__ = (
        UniqueConstraint('ability_index', 'language', 'card'),
    )


class CardAttack(ApiObject):
    __tablename__ = "card_attack"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    index = Column(Integer, primary_key=True, index=True)
    damage = Column(String(200))
    convertedEnergyCost = Column(Integer)


class CardAttackLocalisation(ApiObject):
    __tablename__ = "card_attack_localisation"
    pk = Column(Integer, primary_key=True, autoincrement=True, default=0)
    language = Column(String(20), ForeignKey(Language.code), index=True)
    card = Column(String(20), ForeignKey(CardAttack.card), index=True)
    attack_index = Column(Integer, ForeignKey(CardAttack.index), index=True)
    text = Column(String(500))
    __table_args__ = (
        UniqueConstraint('language', 'card', 'attack_index'),
    )






class EnergyType(ApiObject):
    __tablename__ = "energy_type"
    name = Column(String(20), primary_key=True)

    def __init__(self, name):
        self.name = name

class CardEnergyType(ApiObject):
    __tablename__ = "card_energytype"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    energy = Column(String(20), ForeignKey(EnergyType.name), primary_key=True)


class CardAttackCost(ApiObject):
    __tablename__ = "card_attack_cost"
    pk = Column(Integer, primary_key=True, autoincrement=True)
    card = Column(String(20), ForeignKey(CardAttack.card), index=True)
    attack_index = Column(Integer, ForeignKey(CardAttack.index), index=True)
    energy_type = Column(String(20), ForeignKey(EnergyType.name), index=True)
    amount = Column(Integer)
    __table_args__ = (
        UniqueConstraint('card', 'attack_index', 'energy_type'),
    )

class CardRetreatCost(ApiObject):
    __tablename__ = "card_retreat_cost"
    pk = Column(Integer, primary_key=True, autoincrement=True)
    card = Column(String(20), ForeignKey(Card.id), index=True)
    energy_type = Column(String(20), ForeignKey(EnergyType.name), index=True)
    amount = Column(Integer)
    __table_args__ = (
        UniqueConstraint('card', 'energy_type'),
    )

class CardWeakness(ApiObject):
    __tablename__ = "card_weakness"
    pk = Column(Integer, primary_key=True, autoincrement=True)
    card = Column(String(20), ForeignKey(Card.id), index=True)
    energy_type = Column(String(20), ForeignKey(EnergyType.name), index=True)
    value = Column(String(10))
    __table_args__ = (
        UniqueConstraint('card', 'energy_type'),
    )


class CardNationalPokedexNumbers(ApiObject):
    __tablename__ = "card_NationalPokedexNumbers"
    card = Column(String(20), ForeignKey(Card.id), primary_key=True)
    nationalPokedexNumber = Column(Integer, primary_key=True)


# Deck and constituent fields
# class Deck(ApiObject):
#     __tablename__ = "deck"
#     id = Column(String(20), primary_key=True)
#     set = Column(String(20), ForeignKey('set.id'))
#
#
# class DeckLocalisation(ApiObject):
#     __tablename__ = "deck_localisation"
#     deck = Column(String(20), ForeignKey(Deck.id), primary_key=True)
#     language = Column(String(20), ForeignKey(Language.code), primary_key=True)
#     name = Column(String(20))
#
#
# class DeckType(ApiObject):
#     __tablename__ = "deck_type"
#     deck = Column(String(20), ForeignKey(Deck.id), primary_key=True)
#     energy = Column(String(20), ForeignKey(EnergyType.name), primary_key=True)
#
#
# class DeckCard(ApiObject):
#     __tablename__ = "deck_card"
#     deck = Column(String(20), ForeignKey(Deck.id), primary_key=True)
#     id = Column(String(20), primary_key=True)
#     card = Column(String(20), ForeignKey(Card.id))
#     rarity = Column(String(20), ForeignKey(Rarity.name))

# ed_user = Series('hehe')
# session.merge(ed_user)
# session.commit()
#
# results = session.query(Series).all()
# logger.info(results)
