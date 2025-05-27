from fastapi import APIRouter, Depends, HTTPException
from ..services.scenario_compiler import ScenarioCompiler
from ..models.scenario import CompiledScenario

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

@router.post("/compile/{scenario_id}", response_model=CompiledScenario)
async def compile_scenario(scenario_id: int):
    """Компилирует сценарий из PostgreSQL в MongoDB"""
    compiler = ScenarioCompiler(None)  # Здесь нужна SQLAlchemy сессия
    return await compiler.compile_scenario(scenario_id)

@router.get("/{scenario_id}", response_model=CompiledScenario)
async def get_compiled_scenario(scenario_id: str):
    """Получает скомпилированный сценарий"""
    # Логика получения из MongoDB
    pass
