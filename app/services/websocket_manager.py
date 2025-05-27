from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.player_connections: Dict[str, WebSocket] = {}
        self.master_connections: Dict[str, WebSocket] = {}
    
    async def connect_player(self, websocket: WebSocket, session_id: str, player_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
        self.player_connections[f"{session_id}:{player_id}"] = websocket
    
    async def connect_master(self, websocket: WebSocket, session_id: str, master_id: str):
        await websocket.accept()
        self.master_connections[f"{session_id}:{master_id}"] = websocket
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
        
        # Удаляем из player_connections и master_connections
        keys_to_remove = []
        for key, ws in self.player_connections.items():
            if ws == websocket:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.player_connections[key]
        
        keys_to_remove = []
        for key, ws in self.master_connections.items():
            if ws == websocket:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.master_connections[key]
    
    async def send_personal_message(self, message: dict, session_id: str, player_id: str):
        websocket = self.player_connections.get(f"{session_id}:{player_id}")
        if websocket:
            await websocket.send_json(message)
    
    async def send_to_master(self, message: dict, session_id: str, master_id: str):
        websocket = self.master_connections.get(f"{session_id}:{master_id}")
        if websocket:
            await websocket.send_json(message)
    
    async def broadcast_to_session(self, message: dict, session_id: str):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)

manager = ConnectionManager()
