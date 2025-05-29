from fastapi import APIRouter, HTTPException, Depends, status
from ..services.session_manager import SessionManager
from ..models.session import GameSession, CreateSessionRequest
from ..models.updates import PerformActionRequest
from ..middleware.auth import get_current_active_user, get_current_master
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime
from ..database import get_database
from ..models.scenario import CompiledScenario
from bson import ObjectId

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/list", response_model=List[GameSession])
async def get_sessions(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user = Depends(get_current_active_user)
):
    """Получить список всех активных сессий"""
    try:
        sessions = await db["sessions"].find({"status": "active"}).to_list(length=100)
        return [GameSession(**session) for session in sessions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/my", response_model=List[GameSession])
async def get_my_sessions(
    current_user = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Получает все сессии пользователя"""
    try:
        user_id = str(current_user.id)
        sessions = await db["sessions"].find({
            "$or": [
                {"master_id": user_id},
                {"players.player_id": user_id}
            ]
        }).to_list(length=100)
        return [GameSession(**session) for session in sessions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/create", response_model=GameSession)
async def create_session(
    request: CreateSessionRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user = Depends(get_current_master)  # Только мастера могут создавать сессии
):
    """Создать новую игровую сессию"""
    try:
        # Проверяем существование сценария
        scenario = await db["scenarios"].find_one({"_id": ObjectId(request.scenario_id)})
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сценарий не найден"
            )
        
        # Создаем новую сессию
        session = GameSession(
            scenario_id=request.scenario_id,
            master_id=str(current_user.id),  # Используем ID из токена
            name=request.name,
            status="waiting",
            players=request.players or [],
            current_time=datetime.utcnow(),
            world_state={
                "object_positions": [],
                "triggered_events": [],
                "completed_actions": []
            }
        )
        
        result = await db["sessions"].insert_one(session.dict(by_alias=True))
        session.id = result.inserted_id
        return session
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{session_id}", response_model=GameSession)
async def get_session(
    session_id: str,
    current_user = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Получить информацию о конкретной сессии"""
    try:
        session = await db["sessions"].find_one({"_id": ObjectId(session_id)})
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сессия не найдена"
            )
        
        # Проверяем права доступа (мастер или участник)
        user_id = str(current_user.id)
        if session["master_id"] != user_id and not any(p["player_id"] == user_id for p in session.get("players", [])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этой сессии"
            )
        
        return GameSession(**session)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, ValueError) and "ObjectId" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат ID сессии"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{session_id}/actions")
async def perform_action(
    session_id: str,
    request: PerformActionRequest,
    current_user = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Выполняет действие игрока"""
    try:
        # Проверяем что игрок может выполнять действия в этой сессии
        session = await db["sessions"].find_one({"_id": ObjectId(session_id)})
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сессия не найдена"
            )
        
        user_id = str(current_user.id)
        if not any(p["player_id"] == user_id for p in session.get("players", [])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не участвуете в этой сессии"
            )
        
        # Устанавливаем player_id из токена
        request.player_id = user_id
        
        # Логика выполнения действия и обновления состояния
        # TODO: Реализовать обработку действий
        
        return {"message": "Действие выполнено", "action_id": request.action_id}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, ValueError) and "ObjectId" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат ID сессии"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
