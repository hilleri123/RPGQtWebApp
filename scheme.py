from sqlalchemy import create_engine, Column, Integer, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


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
    description = Column(String)
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
    changeMarkId = Column(Integer, ForeignKey('Mark.id', ondelete='CASCADE'), default=None)
    getGameItemId = Column(Integer, ForeignKey('GameItem.id', ondelete='CASCADE'), default=None, )
    # npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None,) # TODO вроде не нужно
    needGameItemIdsJson = Column(String, default=None, )


class PlayerCharacter(Base):
    __tablename__ = 'PlayerCharacter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    shortDesc = Column(String)
    story = Column(String)


class SceneMap(Base):
    __tablename__ = 'SceneMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)
    isCurrent = Column(Boolean)


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
Session = sessionmaker(bind=engine)


IS_EDITABLE = True

