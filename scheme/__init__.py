from .base import Base, engine, sessionmaker
from .action import PlayerAction
from .map import SceneMap, Location, MapObjectPolygon
from .game import GameItem, NPC, Skill, SkillGroup, Stat, PlayerCharacter, WhereObject, GlobalSession
from .text_data import GameEvent, Note

from contextlib import contextmanager

Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)

@contextmanager
def Session():
    session = SessionMaker()
    yield session
    session.close()