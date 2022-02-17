from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, ForeignKey, DateTime, Date, UniqueConstraint, \
    BINARY, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import hashlib


def AttributesFromArgsDictionary(f):
    # This function is what we "replace" hello with
    def wrapper(self, args):
        for name, value in args.items():
            setattr(self, name, value)

        return f(self, args)  # Call hello

    return wrapper


# def AttributesFromArgsDictionary(f):
#     def __call__(self, cls):
#         def Inner(cls, *args, **kw):
#
#         return Inner


def generate_sid(fields):
    if isinstance(fields, list):
        result = ""
        for field in fields:
            result += str(field)
        return hashlib.sha1(result.encode('utf-8')).digest()
    else:
        return hashlib.sha1(fields.encode('utf-8')).digest()
    # return hashlib.md5("".join(fields).encode('utf-8')).hexdigest()


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


# Parent Attributes / Enums
def models(Base):
    class Series(Base):
        __tablename__ = "series"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(50))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class Language(Base):
        __tablename__ = "language"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        code = Column(String(20))
        name = Column(String(50))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class Legality(Base):
        __tablename__ = "legality"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class Rarity(Base):
        __tablename__ = "rarity"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class SuperType(Base):
        __tablename__ = "supertype"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class Artist(Base):
        __tablename__ = "artist"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(50))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

        def __eq__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.name == other.name

        def __hash__(self):
            return hash(self.sid)

    # Main Objects
    class TCGSet(Base):
        __tablename__ = "tcg_set"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        id = Column(String(20))
        series = Column(String(50), ForeignKey('series.name'))
        printedTotal = Column(Integer)
        total = Column(Integer)
        ptcgoCode = Column(String(20))
        releaseDate = Column(Date)
        updatedAt = Column(DateTime)

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid(self.id)

        # Localization and many-to-many junctions

    class SetLocalisation(Base):
        __tablename__ = "set_localisation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        language = Column(String(20), ForeignKey('language.code'))
        set = Column(String(20), ForeignKey('tcg_set.id'))
        name = Column(String(50))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.language, self.set])

    class SetLegality(Base):
        __tablename__ = "set_legality"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        set = Column(String(20), ForeignKey('tcg_set.id'))
        legality = Column(String(20), ForeignKey('legality.name'))

        def __init__(self, set, legality):
            self.set = set
            self.legality = legality
            self.sid = generate_sid([self.set, self.legality])

    class SetImageType(Base):
        __tablename__ = "set_image_type"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class SetImage(Base):
        __tablename__ = "set_image"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        set = Column(String(20), ForeignKey('tcg_set.id'))
        imageType = Column(String(20), ForeignKey('set_image_type.name'))
        language = Column(String(20), ForeignKey('language.code'))
        url = Column(String(200))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.set, self.imageType, self.language])

        # Card and constituent fields

    class Card(Base):
        __tablename__ = "card"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        id = Column(String(20), comment="generated field from '{set}-{number}'")
        set_id = Column(String(20), ForeignKey('tcg_set.id'))
        set_sid = Column(BINARY)
        number = Column(String(20))
        hp = Column(String(20))
        artist = Column(String(100))
        supertype = Column(String(20), ForeignKey('supertype.name'))
        rarity = Column(String(20), ForeignKey('rarity.name'))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.id])
            self.set_sid = generate_sid([self.set_id])

        # Localization and many-to-many junctions

    class CardLocalisation(Base):
        __tablename__ = "card_localisation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        language = Column(String(20), ForeignKey('language.code'))
        name = Column(String(100))
        flavor_text = Column(String(100))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.language])

    class CardEnergyType(Base):
        __tablename__ = "card_energytype"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        energy = Column(String(20), ForeignKey('energy_type.name'))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.energy])

    class CardImageType(Base):
        __tablename__ = "card_image_type"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid([self.name])

    class CardImage(Base):
        __tablename__ = "card_image"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        imageType = Column(String(20), ForeignKey('card_image_type.name'))
        language = language = Column(String(20), ForeignKey('language.code'))
        url = Column(String(200))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.imageType, self.language])

    class CardLegalityOverride(Base):
        __tablename__ = "card_legality_override"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        legality = Column(String(20), ForeignKey('legality.name'))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.legality])

    class CardEvolution(Base):
        __tablename__ = "card_evolution"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        pokemonName = Column(String(100))
        nationalPokedexNumber = Column(String(5))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.pokemonName])

    class CardAbility(Base):
        __tablename__ = "card_ability"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        index = Column(Integer)
        convertedEnergyCost = Column(Integer)
        abilityType = Column(String(20))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.index])

    class CardAbilityLocalisation(Base):
        __tablename__ = "card_ability_localisation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        pk = Column(Integer, autoincrement=True, default=0)
        card = Column(String(20), ForeignKey('card_ability.card'), index=True)
        ability_index = Column(Integer, ForeignKey('card_ability.index'), index=True)
        language = Column(String(20), ForeignKey('language.code'), index=True)
        text = Column(String(1000))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.ability_index, self.language])

    class CardAttack(Base):
        __tablename__ = "card_attack"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        index = Column(Integer, index=True)
        damage = Column(String(200))
        convertedEnergyCost = Column(Integer)

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.index])

    class CardAttackLocalisation(Base):
        __tablename__ = "card_attack_localisation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        pk = Column(Integer, autoincrement=True, default=0)
        language = Column(String(20), ForeignKey('language.code'), index=True)
        card = Column(String(20), ForeignKey('card_attack.card'), index=True)
        attack_index = Column(Integer, ForeignKey('card_attack.index'), index=True)
        text = Column(String(500))

        # __table_args__ = (
        #     UniqueConstraint('language', 'card', 'attack_index'),
        # )

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.language, self.card, self.attack_index])

    class CardAttackCost(Base):
        __tablename__ = "card_attack_cost"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        pk = Column(Integer, autoincrement=True)
        card = Column(String(20), ForeignKey('card_attack.card'), index=True)
        attack_index = Column(Integer, ForeignKey('card_attack.index'), index=True)
        energy_type = Column(String(20), ForeignKey('energy_type.name'), index=True)
        amount = Column(Integer)

        # __table_args__ = (
        #     UniqueConstraint('card', 'attack_index', 'energy_type'),
        # )

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.attack_index, self.energy_type])

    class EnergyType(Base):
        __tablename__ = "energy_type"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        name = Column(String(20))

        def __init__(self, name):
            self.name = name
            self.sid = generate_sid(self.name)

    class CardRetreatCost(Base):
        __tablename__ = "card_retreat_cost"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        pk = Column(Integer, autoincrement=True)
        card = Column(String(20), ForeignKey('card.id'), index=True)
        energy_type = Column(String(20), ForeignKey('energy_type.name'), index=True)
        amount = Column(Integer)

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.energy_type])

    class CardWeakness(Base):
        __tablename__ = "card_weakness"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        pk = Column(Integer, autoincrement=True)
        card = Column(String(20), ForeignKey('card.id'), index=True)
        energy_type = Column(String(20), ForeignKey('energy_type.name'), index=True)
        value = Column(String(10))

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.energy_type])

    class CardNationalPokedexNumbers(Base):
        __tablename__ = "card_NationalPokedexNumbers"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card = Column(String(20), ForeignKey('card.id'))
        nationalPokedexNumber = Column(Integer)

        @AttributesFromArgsDictionary
        def __init__(self, args):
            self.sid = generate_sid([self.card, self.nationalPokedexNumber])

        # Deck and constituent fields

    class Deck(Base):
        __tablename__ = "deck"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        id = Column(String(20))
        set = Column(String(20), ForeignKey('tcg_set.id'))

        @hybrid_property
        def sid(self):
            return generate_sid([self.deck, self.language])

    class DeckLocalisation(Base):
        __tablename__ = "deck_localisation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        deck = Column(String(20), ForeignKey('deck.id'))
        language = Column(String(20), ForeignKey('language.code'))
        name = Column(String(20))

        @hybrid_property
        def sid(self):
            return generate_sid([self.deck, self.language])

    class DeckType(Base):
        __tablename__ = "deck_type"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        deck = Column(String(20), ForeignKey('deck.id'))
        energy = Column(String(20), ForeignKey('energy_type.name'))

        @hybrid_property
        def sid(self):
            return generate_sid([self.deck, self.energy])

    class DeckCard(Base):
        __tablename__ = "deck_card"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        deck = Column(String(20), ForeignKey('deck.id'))
        id = Column(String(20))
        card = Column(String(20), ForeignKey('card.id'))
        rarity = Column(String(20), ForeignKey('rarity.name'))

        @hybrid_property
        def sid(self):
            return generate_sid([self.deck, self.id])

    objects = {
        'Series': Series,
        'Language': Language,
        'Legality': Legality,
        'Rarity': Rarity,
        'SuperType': SuperType,
        'Artist': Artist,
        'TCGSet': TCGSet,
        'SetLocalisation': SetLocalisation,
        'SetLegality': SetLegality,
        'SetImageType': SetImageType,
        'SetImage': SetImage,
        'Card': Card,
        'CardLocalisation': CardLocalisation,
        'CardEnergyType': CardEnergyType,
        'CardImageType': CardImageType,
        'CardImage': CardImage,
        'CardLegalityOverride': CardLegalityOverride,
        'CardEvolution': CardEvolution,
        'CardAbility': CardAbility,
        'CardAbilityLocalisation': CardAbilityLocalisation,
        'CardAttack': CardAttack,
        'CardAttackLocalisation': CardAttackLocalisation,
        'CardAttackCost': CardAttackCost,
        'EnergyType': EnergyType,
        'CardRetreatCost': CardRetreatCost,
        'CardWeakness': CardWeakness,
        'CardNationalPokedexNumbers': CardNationalPokedexNumbers
    }
    return AttrDict(objects)
# Base.metadata.create_all()
# Session = sessionmaker(bind=engine)()
