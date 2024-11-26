from sqlalchemy import create_engine, Column, Integer, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import sqlite3
import os

DB_URL = 'rpgtool.db'

if os.path.exists(DB_URL):
    os.remove(DB_URL)

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
    needSkillIdsConditionsJson = Column(String, default=None,)
    changeMarkId = Column(Integer, ForeignKey('Mark.id', ondelete='CASCADE'), default=None)
    getGameItemId = Column(Integer, ForeignKey('GameItem.id', ondelete='CASCADE'), default=None,)
    # npcId = Column(Integer, ForeignKey('NPC.id', ondelete='CASCADE'), default=None,) # TODO вроде не нужно
    needGameItemIdsJson = Column(String, default=None,)

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
# Добавьте остальные классы аналогично...

# Пример создания базы данных
engine = create_engine(f'sqlite:///{DB_URL}')
Base.metadata.create_all(engine)


class NULL:
    def __repr__(self):
        return "NULL"

def dump_data(source_db_path, file_name):
    # Подключение к исходной базе данных
    source_conn = sqlite3.connect(source_db_path)
    source_cursor = source_conn.cursor()

    if os.path.exists(file_name):
        os.remove(file_name)

    res = []

    try:
        # Получение списка таблиц из исходной базы данных
        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table_name in tables:
            table_name = table_name[0]

            # Извлечение всех данных из текущей таблицы
            source_cursor.execute(f"SELECT * FROM {table_name}")
            rows = source_cursor.fetchall()

            # Получение информации о столбцах таблицы
            source_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in source_cursor.fetchall()]

            # Формирование строки с именами столбцов для вставки
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["?"] * len(columns))

            def t(row):
                return tuple(NULL() if i is None else i for i in row)

            tmp_rows = [f"{t(row).__repr__()}" for row in rows]
            
            if len(rows) > 0:
                res.append(f"INSERT INTO {table_name} ({columns_str}) VALUES {','.join(tmp_rows)} ;")
                print(res[-1])

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрытие подключений
        source_conn.close()
        
    with open(file_name, 'a') as f:
        tmp_items = []
        f.write('\n'.join(res))