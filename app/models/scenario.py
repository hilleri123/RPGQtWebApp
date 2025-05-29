from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Недопустимый ObjectId")
        return ObjectId(v)

class Skill(BaseModel):
    id: int
    name: str

class SkillGroup(BaseModel):
    id: int
    name: str
    skills: List[Skill]

class BaseStat(BaseModel):
    skill_id: int
    init_value: int

class Body(BaseModel):
    id: int
    name: str
    img: str
    icon: str
    base_stats: List[BaseStat]

class GameItemScheme(BaseModel):
    id: int
    name: str
    text: str
    data: Dict[str, Any]

class Rules(BaseModel):
    id: int
    name: str
    skill_groups: List[SkillGroup]
    bodies: List[Body]
    game_item_schemes: List[GameItemScheme]

class MapObject(BaseModel):
    id: int
    name: str
    target_location_id: Optional[int]
    is_shown: bool
    polygon_list: List[List[int]]
    color: str

class Location(BaseModel):
    id: int
    name: str
    description: str
    file: str
    parent_location_id: Optional[int]
    map_objects: List[MapObject]

class NPC(BaseModel):
    id: int
    name: str
    story: str
    body_id: int

class GameItem(BaseModel):
    id: int
    unique_name: str
    item_scheme_id: int

class Requirement(BaseModel):
    skill_id: int
    skill_value: int
    threshold: bool

class ActionLocation(BaseModel):
    location_id: int
    npc_id: Optional[int]
    item_scheme_id: Optional[int]

class PlayerAction(BaseModel):
    id: int
    description_for_master: str
    description_for_players: str
    add_time_secs: int
    requirements: List[Requirement]
    locations: List[ActionLocation]

class Note(BaseModel):
    id: int
    name: str
    text: str
    allowed_characters: List[int]

class TimeEvent(BaseModel):
    id: int
    name: str
    text: str
    start_time: datetime
    end_time: datetime
    note_id: Optional[int]

class ScenarioInfo(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = ""
    intro: Optional[str] = ""
    icon: Optional[str] = ""
    difficulty: Optional[str] = "Средняя"
    min_players: Optional[int] = 1
    max_players: Optional[int] = 4
    created: Optional[datetime] = Field(default_factory=datetime.utcnow)

class CompiledScenario(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    type: str = "compiled_scenario"
    scenario: ScenarioInfo
    rules: Rules
    locations: List[Location]
    npcs: List[NPC]
    game_items: List[GameItem]
    player_actions: List[PlayerAction]
    notes: List[Note]
    time_events: List[TimeEvent]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
