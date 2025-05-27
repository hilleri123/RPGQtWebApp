from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/player/{session_id}/{player_id}")
async def websocket_player(websocket: WebSocket, session_id: str, player_id: str):
    await manager.connect_player(websocket, session_id, player_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Обработка сообщений от игрока
            await manager.broadcast_to_session(data, session_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

@router.websocket("/ws/master/{session_id}/{master_id}")
async def websocket_master(websocket: WebSocket, session_id: str, master_id: str):
    await manager.connect_master(websocket, session_id, master_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Обработка команд мастера
            if data["type"] == "spawn_object":
                # Логика создания объекта
                pass
            elif data["type"] == "move_object":
                # Логика перемещения объекта
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
