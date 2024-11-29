from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import ColorType
from colour import Color


SKILL_GROUP = ("Научные", "Технические", "Межличностные", "Основные")

DB_URL = 'data/rpgtool.db'


Base = declarative_base()


class GameCondition(Base):
    __tablename__ = 'GameCondition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    markConditionJson = Column(String, default=None)
    locationId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    playerActionId = Column(Integer, ForeignKey('PlayerAction.id', ondelete='CASCADE'), default=None)
    npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None)
    travelToLocationId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    text = Column(String, default=None)


class GameItem(Base):
    __tablename__ = 'GameItem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    text = Column(String)


class Location(Base):
    __tablename__ = 'Location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    shape = Column(Integer)
    offsetX = Column(Integer)
    offsetY = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    icon_file_path = Column(String)
    description = Column(String)
    is_shown = Column(Integer, default=0) #Как boolean, но 2 - это значит конст
    mapId = Column(Integer, ForeignKey('SceneMap.id', ondelete='CASCADE'))


class Mark(Base):
    __tablename__ = 'Mark'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    isActivated = Column(Boolean)
    status = Column(Integer)


class NPC(Base):
    __tablename__ = 'NPC'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    descriptionText = Column(String)
    isDead = Column(Boolean)


class PlayerAction(Base):
    __tablename__ = 'PlayerAction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    needSkillIdsConditionsJson = Column(String, default=None, )
    changeMarkId = Column(Integer, ForeignKey('Mark.id'), default=None)
    getGameItemId = Column(Integer, ForeignKey('GameItem.id'), default=None, )
    is_activated = Column(Boolean, default=False)
    needGameItemIdsJson = Column(String, default=None)
    add_time = Column(DateTime, default=None)


class Note(Base):
    __tablename__ = 'Note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    xml_text = Column(String)
    action_id = Column(Integer, ForeignKey('PlayerAction.id'), default=None)


class GlobalMap(Base):
    __tablename__ = 'GlobalMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)
    time = Column(DateTime)


class SceneMap(Base):
    __tablename__ = 'SceneMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)
    isCurrent = Column(Boolean)
    offsetX = Column(Integer)
    offsetY = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    is_shown = Column(Integer, default=0) #Как boolean, но 2 - это значит конст
    icon_file_path = Column(String)


class PlayerCharacter(Base):
    __tablename__ = 'PlayerCharacter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    shortDesc = Column(String)
    story = Column(String)
    time = Column(DateTime)
    color = Column(ColorType)
    address = Column(String)
    player_locked = Column(Boolean)
    map_id = Column(Integer, ForeignKey('Location.id'))
    location_id = Column(Integer, ForeignKey('SceneMap.id'))


class Skill(Base):
    __tablename__ = 'Skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    groupName = Column(String)


class Stat(Base):
    __tablename__ = 'Stats'
    characterId = Column(Integer, ForeignKey('PlayerCharacter.id', ondelete='CASCADE'), primary_key=True)
    skillId = Column(Integer, ForeignKey('Skills.id', ondelete='CASCADE'), primary_key=True)
    initValue = Column(Integer)
    value = Column(Integer)


class WhereObject(Base):
    __tablename__ = 'WhereObject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gameItemId = Column(Integer, ForeignKey('GameItem.id', ondelete='CASCADE'), nullable=False)
    npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None)
    locationId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    __table_args__ = (
        UniqueConstraint('gameItemId', name='uq_game_item_id'),
    )


engine = create_engine(f'sqlite:///{DB_URL}')
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

def Session():
    return session


IS_EDITABLE = True

