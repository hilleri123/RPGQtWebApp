from datetime import datetime
from typing import List, Optional
from ..models.session import GameSession, CreateSessionRequest, Player
from ..models.scene import PlayerScene
from ..database import get_database
from bson import ObjectId

class SessionManager:
    async def create_session(self, request: CreateSessionRequest) -> GameSession:
        """Создает новую игровую сессию"""
        session = GameSession(
            scenario_id=request.scenario_id,
            master_id=request.master_id,
            current_time=datetime.utcnow(),
            players=request.players,
            world_state={
                "object_positions": [],
                "triggered_events": [],
                "completed_actions": []
            }
        )
        
        db = await get_database()
        result = await db.game_sessions.insert_one(session.dict(by_alias=True))
        session.id = result.inserted_id
        
        # Создаем сцены для каждого игрока
        for player in request.players:
            await self.create_player_scene(str(session.id), player.player_id)
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[GameSession]:
        """Получает игровую сессию по ID"""
        db = await get_database()
        session_data = await db.game_sessions.find_one({"_id": ObjectId(session_id)})
        
        if session_data:
            return GameSession(**session_data)
        return None
    
    async def create_player_scene(self, session_id: str, player_id: str) -> PlayerScene:
        """Создает сцену для игрока"""
        # Логика создания сцены на основе текущего состояния сессии
        scene = PlayerScene(
            session_id=session_id,
            player_id=player_id,
            current_location={
                "id": 1,
                "name": "Стартовая локация",
                "description": "Описание",
                "file": "map_url",
                "map_objects": []
            },
            visible_objects={
                "npcs": [],
                "game_items": [],
                "other_players": []
            },
            available_actions=[],
            character_state={
                "name": "Персонаж",
                "stats": [],
                "inventory": []
            }
        )
        
        db = await get_database()
        await db.player_scenes.insert_one(scene.dict(by_alias=True))
        
        return scene
    
    async def update_player_scene(self, session_id: str, player_id: str):
        """Обновляет сцену игрока на основе текущего состояния сессии"""
        # Логика обновления сцены
        pass
