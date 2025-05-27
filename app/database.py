from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://admin:admin@mongodb:27017/game_sessions_db?authSource=admin"
    database_name: str = "game_sessions_db"
    sqlalchemy_database_url: str = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'postgres')}@db:5432/{os.getenv('POSTGRES_DB', 'rpg_sessions')}"
    secret_key: str = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    class Config:
        env_file = ".env"

settings = Settings()

# MongoDB клиент
class Database:
    client: AsyncIOMotorClient = None
    
database = Database()

# PostgreSQL для пользователей и исходных данных
engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base для SQLAlchemy моделей
Base = declarative_base()

async def get_database() -> AsyncIOMotorClient:
    return database.client[settings.database_name]

def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def connect_to_mongo():
    database.client = AsyncIOMotorClient(settings.mongodb_url)
    print("Подключение к MongoDB установлено")
    
    # Проверка подключения
    try:
        await database.client.admin.command('ping')
        print("MongoDB ping успешен")
    except Exception as e:
        print(f"Ошибка подключения к MongoDB: {e}")

async def close_mongo_connection():
    database.client.close()
    print("Подключение к MongoDB закрыто")

def create_tables():
    """Создает все таблицы в PostgreSQL"""
    from .models.auth import Base as AuthBase
    AuthBase.metadata.create_all(bind=engine)
    print("Таблицы пользователей созданы")
