from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .scenario import PyObjectId

class SceneMapObject(BaseModel):
    id: int
    name: str
    is_shown: bool
    polygon_list: List[List[int]]
    color: str
    icon: Optional[str]

class CurrentLocation(BaseModel):
    id: int
    name: str
    description: str
    file: str
    map_objects: List[SceneMapObject]

class VisibleNPC(BaseModel):
    id: int
    name: str
    story: str
    body: dict

class VisibleGameItem(BaseModel):
    id: int
    unique_name: str
    scheme: dict

class OtherPlayer(BaseModel):
    character_name: str
    color: str

class ActionRequirement(BaseModel):
    skill_name: str
    required_value: int
    current_value: int
    can_perform: bool

class ActionTarget(BaseModel):
    type: str
    id: int

class AvailableAction(BaseModel):
    id: int
    description: str
    target: ActionTarget
    requirements: List[ActionRequirement]

class CharacterStat(BaseModel):
    skill_name: str
    current_value: int

class CharacterState(BaseModel):
    name: str
    stats: List[CharacterStat]
    inventory: List[dict]

class VisibleObjects(BaseModel):
    npcs: List[VisibleNPC]
    game_items: List[VisibleGameItem]
    other_players: List[OtherPlayer]

class PlayerScene(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    type: str = "player_scene"
    session_id: str
    player_id: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    current_location: CurrentLocation
    visible_objects: VisibleObjects
    available_actions: List[AvailableAction]
    character_state: CharacterState

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
