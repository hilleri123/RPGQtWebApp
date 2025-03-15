from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy_utils import ColorType


class SceneMap(Base):
    __tablename__ = 'SceneMap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filePath = Column(String)


class Location(Base):
    __tablename__ = 'Location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    leads_to = Column(Integer, ForeignKey('SceneMap.id'))


class MapObjectPolygon(Base):
    __tablename__ = 'MapObject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    map_id = Column(Integer, ForeignKey('SceneMap.id'))
    location_id = Column(Integer, ForeignKey('Location.id'))
    is_shown = Column(Boolean, default=False)
    is_filled = Column(Boolean, default=False)
    is_line = Column(Boolean, default=False)
    color = Column(ColorType)
    poygon_list_json = Column(String, default='[]')
    icon_file_path = Column(String)