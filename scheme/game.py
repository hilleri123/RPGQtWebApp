from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy_utils import ColorType


class GameItem(Base):
    __tablename__ = 'GameItem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    text = Column(String, default='')
    bonusesJson = Column(String, default='')



class NPC(Base):
    __tablename__ = 'NPC'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path_to_img = Column(String)
    is_enemy = Column(Boolean, default=False)
    skillIdsJson = Column(String, default='[]')
    description = Column(String)
    isDead = Column(Boolean)


class SkillGroup(Base):
    __tablename__ = 'SkillGroup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Skill(Base):
    __tablename__ = 'Skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    groupId = Column(Integer, ForeignKey('SkillGroup.id', ondelete='CASCADE'), nullable=False)


class Stat(Base):
    __tablename__ = 'Stats'
    characterId = Column(Integer, ForeignKey('PlayerCharacter.id', ondelete='CASCADE'), primary_key=True)
    skillId = Column(Integer, ForeignKey('Skills.id', ondelete='CASCADE'), primary_key=True)
    initValue = Column(Integer, default=0)
    value = Column(Integer, default=0)



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



class WhereObject(Base):
    __tablename__ = 'WhereObject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gameItemId = Column(Integer, ForeignKey('GameItem.id', ondelete='CASCADE'), nullable=False)
    npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None)
    locationId = Column(Integer, ForeignKey('Location.id', ondelete='CASCADE'), default=None)
    playerId = Column(Integer, ForeignKey('PlayerCharacter.id', ondelete='CASCADE'), default=None)
    __table_args__ = (
        UniqueConstraint('gameItemId', name='uq_game_item_id'),
    )


class GlobalSession(Base):
    __tablename__ = 'GlobalSession'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filePath = Column(String)
    intro = Column(String)
    time = Column(DateTime)
    start_time = Column(DateTime)
    scenario_name = Column(String)
    scenario_file_path = Column(String)
