from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_postgres_db
from ..models.auth import UserCreate, UserResponse, Token, LoginRequest
from ..services.auth_service import AuthService, UserService, ACCESS_TOKEN_EXPIRE_MINUTES
from ..middleware.auth import get_current_active_user, get_current_master

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_postgres_db)):
    """Регистрация нового пользователя"""
    user_service = UserService(db)
    user = user_service.create_user(user_data)
    return user

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_postgres_db)):
    """Авторизация пользователя"""
    user_service = UserService(db)
    user = user_service.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # в секундах
    }

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_postgres_db)
):
    """OAuth2-совместимый endpoint для получения токена"""
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_active_user)):
    """Получить информацию о текущем пользователе"""
    return current_user

@router.get("/masters-only")
async def masters_only_endpoint(current_user = Depends(get_current_master)):
    """Пример защищенного endpoint только для мастеров"""
    return {"message": f"Hello master {current_user.username}!"}
