from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection, create_tables
from .routers import scenarios, sessions, websocket, auth

app = FastAPI(
    title="Game Sessions API",
    description="API для управления игровыми сессиями",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js default port
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://web-client:3000",  # Docker service name
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    expose_headers=["*"],
    max_age=3600,
)

@app.on_event("startup")
async def startup_event():
    # Создаем таблицы пользователей
    create_tables()
    # Подключаемся к MongoDB
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Регистрация роутов
app.include_router(auth.router)  # Роуты авторизации
app.include_router(scenarios.router)
app.include_router(sessions.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Game Sessions API запущен"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
