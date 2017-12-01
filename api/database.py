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
    code = Column(String)

    items = relationship("PlayersItemsTable", back_populates="player")

    def __repr__(self):
        return "<Players(name={})>".format(self.name)


class LevelsTable(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Levels(name={})>".format(self.name)


class ItemsTable(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    status = Column(String)
    question = Column(String)
    answer = Column(String)
    item_type = Column(String)
    level_id = Column(Integer, ForeignKey("levels.id"))

    players_items = relationship("PlayersItemsTable", back_populates="item")

    def __repr__(self):
        return "<Items(question={}, level={}, status={})>".format(self.question, self.level_id, self.status)


class PlayersItemsTable(Base):
    __tablename__ = 'players_items'

    id = Column(Integer, primary_key=True)
    bonus = Column(String)
    player_id = Column(Integer, ForeignKey("players.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    player = relationship("PlayersTable", back_populates="items")
    item = relationship("ItemsTable", back_populates="players_items")

    def __repr__(self):
        return "<PlayersItems(player={})>".format(self.player)
