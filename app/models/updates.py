from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .scenario import PyObjectId

class ObjectChange(BaseModel):
    type: str
    id: int
    location_id: int

class CharacterChanges(BaseModel):
    stats: List[Dict[str, Any]]

class SceneUpdates(BaseModel):
    new_objects: List[ObjectChange]
    removed_objects: List[ObjectChange]
    character_changes: Dict[str, CharacterChanges]

class WorldStateChanges(BaseModel):
    triggered_notes: List[int]
    time_advance_secs: int

class UpdateData(BaseModel):
    action_id: int
    player_id: str
    result: str
    changes: Dict[str, Any]
    affected_players: List[str]
    scene_updates: SceneUpdates
    master_message: str
    player_message: str

class GameUpdate(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    type: str = "game_update"
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    update_type: str
    data: UpdateData

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class PerformActionRequest(BaseModel):
    action_id: int
    player_id: str
    target_id: Optional[int] = None
