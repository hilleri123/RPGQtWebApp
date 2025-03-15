from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey

class GameEvent(Base):
    __tablename__ = 'GameEvent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    xml_text = Column(String)
    happend = Column(Boolean, default=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class Note(Base):
    __tablename__ = 'Note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    xml_text = Column(String)
    player_shown_json = Column(String, default='[]')
    target_player_shown_json = Column(String, default='[]')
    action_id = Column(Integer, ForeignKey('PlayerAction.id'), default=None)

