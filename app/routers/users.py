from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import UserCreate, UserResponse, UserStatisticsResponse
from app import crud

router = APIRouter()


# User
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создать нового пользователя.
    
    - **name**: имя пользователя
    - **email**: email пользователя (уникальный)
    """
    existing = db.query(crud.User).filter(crud.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    return crud.create_user(db, user)


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Получить список всех пользователей"""
    return crud.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретном пользователе"""
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# User Stats
@router.get("/{user_id}/statistics", response_model=UserStatisticsResponse)
def get_user_statistics(
    user_id: int,
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    db: Session = Depends(get_db)
):
    """
    Получить агрегированную статистику по всем устройствам пользователя.
    
    Возвращает:
    - **aggregated_stats**: объединённая статистика по всем устройствам
    - **devices_stats**: статистика для каждого устройства отдельно
    
    - start_time: опционально, начало периода
    - end_time: опционально, конец периода
    """
    stats = crud.get_user_statistics(db, user_id, start_time, end_time)
    if not stats:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return stats