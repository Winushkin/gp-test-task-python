from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/devices_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=False, 
    pool_pre_ping=True 
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    """Зависимость для FastAPI - предоставляет сессию БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()