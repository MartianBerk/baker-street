from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from config import settings

config = settings(["OWNER", "PASS", "HOST", "PORT", "SOURCE"])

Session = sessionmaker(autoflush=False)
Base = declarative_base()
engine = create_engine('postgresql://{OWNER}:{PASS}@{HOST}:{PORT}/{SOURCE}'.format(**config))


def get_session():
    return Session(bind=engine)


class PlayersTable(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    items = relationship("PlayersItemsTable", back_populates="player")

    def __repr__(self):
        return "<Players(name={})>".format(self.name)


class LevelsTable(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    locations = relationship("LocationsTable", back_populates="level")

    def __repr__(self):
        return "<Levels(name={})>".format(self.name)


class LocationsTable(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    level_id = Column(Integer, ForeignKey("levels.id"))

    level = relationship("LevelsTable", back_populates="locations")
    items = relationship("ItemsTable", back_populates="location")

    def __repr__(self):
        return "<Locations(name={}, level={}, items={})>".format(self.name, self.level, self.items)


class ItemsTable(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    status = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("LocationsTable", back_populates="items")
    players_items = relationship("PlayersItemsTable", back_populates="item")

    def __repr__(self):
        return "<Items(name={}, code={}, location={})>".format(self.name, self.code, self.location)


class PlayersItemsTable(Base):
    __tablename__ = 'players_items'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    player = relationship("PlayersTable", back_populates="items")
    item = relationship("ItemsTable", back_populates="players_items")

    def __repr__(self):
        return "<PlayersItems(player={})>".format(self.player)
