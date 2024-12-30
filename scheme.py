from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import ColorType
from colour import Color
import os


SKILL_GROUP = ("Научные", "Технические", "Межличностные", "Основные")

DEFAULT_DIR = 'data'
IMGS_DIR = f'{DEFAULT_DIR}/imgs'
ICONS_DIR = f'{DEFAULT_DIR}/icons'
NPC_ICONS_DIR = f'{DEFAULT_DIR}/npc_icons'
TMP_DIR = f'{DEFAULT_DIR}/tmp'
GLOBAL_MAP_PATH = f'{TMP_DIR}/global_map.png'
CURR_MAP_PATH = f'{TMP_DIR}/curr_map.png'
DB_URL = f'{DEFAULT_DIR}/rpgtool.db'

for d in [DEFAULT_DIR, IMGS_DIR, ICONS_DIR, TMP_DIR, NPC_ICONS_DIR]:
    if not os.path.exists(d):
        os.mkdir(d)

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
    name = Column(String, default='')
    text = Column(String, default='')


class Location(Base):
    __tablename__ = 'Location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    shape = Column(Integer, default=0)
    offsetX = Column(Integer, default=0)
    offsetY = Column(Integer, default=0)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
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
    status = Column(Integer, default=0)


class NPC(Base):
    __tablename__ = 'NPC'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path_to_img = Column(String)
    is_enemy = Column(String, default=False)
    skillIdsJson = Column(String, default='[]')
    description = Column(String)
    isDead = Column(Boolean)


class PlayerAction(Base):
    __tablename__ = 'PlayerAction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    needSkillIdsConditionsJson = Column(String, default='[]', )
    changeMarkId = Column(Integer, ForeignKey('Mark.id'), default=None)
    getGameItemId = Column(Integer, ForeignKey('GameItem.id'), default=None, )
    is_activated = Column(Boolean, default=False)
    needGameItemIdsJson = Column(String, default=None)
    add_time_secs = Column(Integer, default=None)


class Note(Base):
    __tablename__ = 'Note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    xml_text = Column(String)
    player_shown_json = Column(String, default='[]')
    action_id = Column(Integer, ForeignKey('PlayerAction.id'), default=None)


class GlobalMap(Base):
    __tablename__ = 'GlobalMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)
    intro = Column(String)
    time = Column(DateTime)
    start_time = Column(DateTime)


class SceneMap(Base):
    __tablename__ = 'SceneMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)
    isCurrent = Column(Boolean)
    offsetX = Column(Integer, default=0)
    offsetY = Column(Integer, default=0)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
    is_shown = Column(Integer, default=0) #Как boolean, но 2 - это значит конст
    icon_file_path = Column(String)


class MapObjectPolygon(Base):
    __tablename__ = 'MapObject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    global_map_id = Column(Integer, ForeignKey('GlobalMap.id'))
    map_id = Column(Integer, ForeignKey('SceneMap.id'))
    is_shown = Column(Boolean, default=False)
    is_filled = Column(Boolean, default=False)
    is_line = Column(Boolean, default=False)
    color = Column(ColorType)
    poygon_list_json = Column(String, default='[]')


class PlayerCharacter(Base):
    __tablename__ = 'PlayerCharacter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path_to_img = Column(String)
    shortDesc = Column(String)
    story = Column(String)
    time = Column(DateTime)
    color = Column(ColorType)
    address = Column(String)
    player_locked = Column(Boolean)
    map_id = Column(Integer, ForeignKey('SceneMap.id'))
    location_id = Column(Integer, ForeignKey('Location.id'))


class Skill(Base):
    __tablename__ = 'Skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    groupName = Column(String)


class Stat(Base):
    __tablename__ = 'Stats'
    characterId = Column(Integer, ForeignKey('PlayerCharacter.id', ondelete='CASCADE'), primary_key=True)
    skillId = Column(Integer, ForeignKey('Skills.id', ondelete='CASCADE'), primary_key=True)
    initValue = Column(Integer, default=0)
    value = Column(Integer, default=0)


class WhereObject(Base):
    __tablename__ = 'WhereObject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gameItemId = Column(Integer, ForeignKey('GameItem.id', ondelete='CASCADE'), nullable=False)
    npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None)
    locationId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    playerId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    __table_args__ = (
        UniqueConstraint('gameItemId', name='uq_game_item_id'),
    )


class GameEvent(Base):
    __tablename__ = 'GameEvent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    xml_text = Column(String)
    happend = Column(Boolean, default=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


engine = create_engine(f'sqlite:///{DB_URL}')
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

def Session():
    return session


IS_EDITABLE = True

