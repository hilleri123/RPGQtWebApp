from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .scenario import PyObjectId

class CharacterStat(BaseModel):
    skill_id: int
    current_value: int

class Character(BaseModel):
    id: int
    name: str
    short_desc: str
    story: str
    body_id: int
    current_location_id: int
    stats: List[CharacterStat]

class Player(BaseModel):
    player_id: str
    character: Character
    color: str
    is_locked: bool

class ObjectPosition(BaseModel):
    type: str  # "npc", "game_item"
    id: int
    location_id: int
    owner_type: Optional[str] = None
    owner_id: Optional[int] = None

class CompletedAction(BaseModel):
    action_id: int
    player_id: str
    completed_at: datetime
    result: str

class WorldState(BaseModel):
    object_positions: List[ObjectPosition]
    triggered_events: List[int]
    completed_actions: List[CompletedAction]

class GameSession(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    type: str = "game_session"
    scenario_id: str
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    master_id: str
    current_time: datetime
    players: List[Player]
    world_state: WorldState

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class CreateSessionRequest(BaseModel):
    scenario_id: str
    master_id: str
    players: List[Player]

class JoinSessionRequest(BaseModel):
    player_id: str
    character: Character
    color: str
