from sqlalchemy import create_engine, Column, BINARY, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

from download_tcgapi.sql_data_classes import generate_sid, AttrDict


def init_sql(connection_string):
    engine = create_engine(connection_string)
    Base = declarative_base(bind=engine)
    models = enrichment_models(Base)
    Session = sessionmaker(bind=engine)()

    return AttrDict({
        'engine': engine,
        'Base': Base,
        'models': models,
        'Session': Session,
    })


def enrichment_models(Base):
    class CardVariations(Base):
        __tablename__ = "card_variation"
        auto_id = Column(Integer, primary_key=True, autoincrement=True)
        sid = Column(BINARY)
        card_id = Column(String(20))
        card_sid = Column(BINARY)
        tcg_variation = Column(String(20))
        price_market = Column(String(20))

        def __init__(self, card_id, tcg_variation, price_market=None):
            self.card_id = card_id
            self.tcg_variation = tcg_variation
            self.price_market = price_market
            self.card_sid = generate_sid([self.card_id])
            self.sid = generate_sid([self.card_id, self.tcg_variation])

    objects = {
        'CardVariations': CardVariations
    }

    return AttrDict(objects)
