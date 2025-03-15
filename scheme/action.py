from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey



class PlayerAction(Base):
    __tablename__ = 'PlayerAction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    needSkillIdsConditionsJson = Column(String, default='[]', )
    is_activated = Column(Boolean, default=False)
    needGameItemIdsJson = Column(String, default=None)
    add_time_secs = Column(Integer, default=None)