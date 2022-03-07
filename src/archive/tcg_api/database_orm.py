from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, ForeignKey, DateTime, Date, UniqueConstraint, \
    BINARY, LargeBinary
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import hashlib

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class ORM_Class:
    engine: ...
    Base: ...
    models: ...
    Session: ...

    def __init__(self, connection_string, reset_database=False):
        self.engine = create_engine(connection_string)
        self.base = declarative_base(bind=self.engine)
        self.models = self.Models(self.base)
        self.Session = sessionmaker(bind=self.engine)()

        if reset_database:
            self.reset_database()

    def reset_database(self):
        print("Wiping and refreshing database")
        self.base.metadata.drop_all(bind=self.engine, checkfirst=True)
        self.base.metadata.create_all(self.engine)

    def Models(self, Base):
        class ApiObject(Base):
            __abstract__ = True
            __tablename__ = "ApiObject"
            __table_args__ = {"schema": "landing_tcgapi"}

            id = Column(String(20), primary_key=True)
            data = Column(JSON)

            def __repr__(self):
                return f"<{self.__tablename__}(id='{self.id})"

        class Set(ApiObject):
            __tablename__ = "set"

        class Card(ApiObject):
            __tablename__ = "card"

        objects = {
            'ext_sets': Set,
            'ext_cards': Card,
        }
        return AttrDict(objects)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
