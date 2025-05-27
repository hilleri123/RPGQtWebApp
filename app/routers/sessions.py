from fastapi import APIRouter, HTTPException, Depends
from ..services.session_manager import SessionManager
from ..models.session import GameSession, CreateSessionRequest
from ..models.updates import PerformActionRequest
from ..middleware.auth import get_current_active_user, get_current_master

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=GameSession)
async def create_session(
    request: CreateSessionRequest,
    current_user = Depends(get_current_master)  # Только мастера могут создавать сессии
):
    """Создает новую игровую сессию"""
    # Добавляем мастера из токена
    request.master_id = str(current_user.id)
    
    manager = SessionManager()
    return await manager.create_session(request)

@router.get("/{session_id}", response_model=GameSession)
async def get_session(
    session_id: str,
    current_user = Depends(get_current_active_user)
):
    """Получает игровую сессию"""
    manager = SessionManager()
    session = await manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    # Проверяем права доступа (мастер или участник)
    user_id = str(current_user.id)
    if session.master_id != user_id and not any(p.player_id == user_id for p in session.players):
        raise HTTPException(status_code=403, detail="Нет доступа к этой сессии")
    
    return session

@router.post("/{session_id}/actions")
async def perform_action(
    session_id: str,
    request: PerformActionRequest,
    current_user = Depends(get_current_active_user)
):
    """Выполняет действие игрока"""
    # Проверяем что игрок может выполнять действия в этой сессии
    manager = SessionManager()
    session = await manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    user_id = str(current_user.id)
    if not any(p.player_id == user_id for p in session.players):
        raise HTTPException(status_code=403, detail="Вы не участвуете в этой сессии")
    
    # Устанавливаем player_id из токена
    request.player_id = user_id
    
    # Логика выполнения действия и обновления состояния
    return {"message": "Действие выполнено", "action_id": request.action_id}

@router.get("/my/sessions")
async def get_my_sessions(current_user = Depends(get_current_active_user)):
    """Получает все сессии пользователя"""
    # Здесь должна быть логика поиска сессий где пользователь мастер или игрок
    return {"sessions": [], "user_id": current_user.id}
