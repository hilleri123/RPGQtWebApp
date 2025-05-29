from fastapi import APIRouter, Depends, HTTPException, status
from ..services.scenario_compiler import ScenarioCompiler
from ..models.scenario import CompiledScenario, ScenarioInfo
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from ..database import get_database
from ..middleware.auth import get_current_active_user
from bson import ObjectId

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
)

@router.post("/compile/{scenario_id}", response_model=CompiledScenario)
async def compile_scenario(
    scenario_id: int,
    current_user = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Компилирует сценарий из PostgreSQL в MongoDB"""
    try:
        compiler = ScenarioCompiler(None)  # Здесь нужна SQLAlchemy сессия
        compiled = await compiler.compile_scenario(scenario_id)
        
        # Сохраняем скомпилированный сценарий в MongoDB
        await db["scenarios"].insert_one(compiled.dict(by_alias=True))
        
        return compiled
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/list", response_model=List[ScenarioInfo])
async def get_scenarios(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user = Depends(get_current_active_user)
):
    """Получить список всех доступных сценариев с кратким описанием"""
    try:
        # Изменяем запрос, чтобы получить все сценарии
        scenarios = await db["scenarios"].find().to_list(length=100)
        if not scenarios:
            return []
        
        # Преобразуем каждый сценарий в ScenarioInfo
        scenario_list = []
        for scenario in scenarios:
            try:
                compiled = CompiledScenario(**scenario)
                scenario_list.append(compiled.scenario)
            except Exception as e:
                print(f"Error processing scenario {scenario.get('_id')}: {str(e)}")
                continue
        
        return scenario_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{scenario_id}", response_model=CompiledScenario)
async def get_scenario(
    scenario_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user = Depends(get_current_active_user)
):
    """Получить полную информацию о сценарии"""
    try:
        # Пробуем преобразовать строку в ObjectId
        try:
            scenario_obj_id = ObjectId(scenario_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат ID сценария"
            )
        
        scenario = await db["scenarios"].find_one({"_id": scenario_obj_id})
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сценарий не найден"
            )
        
        return CompiledScenario(**scenario)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
