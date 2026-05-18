from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import MeasurementCreate, MeasurementResponse, DeviceStatisticsResponse
from app import crud

router = APIRouter()

# Measurments
@router.post("/measurements", response_model=MeasurementResponse)
def add_measurement(
    device_id: int,
    measurement: MeasurementCreate,
    db: Session = Depends(get_db)
):
    """
    Добавить новое измерение для устройства.
    
    Формат данных: {"x": float, "y": float, "z": float}
    """
    result = crud.create_measurement(db, device_id, measurement)
    if not result:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return result


@router.get("/measurements", response_model=list[MeasurementResponse])
def get_measurements(
    device_id: int,
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    db: Session = Depends(get_db)
):
    """
    Получить все измерения устройства.
    
    - start_time: опционально, начало временного диапазона
    - end_time: опционально, конец временного диапазона
    """
    device = crud.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    
    return crud.get_measurements_by_device(db, device_id, start_time, end_time)


# Statistics
@router.get("/statistics", response_model=DeviceStatisticsResponse)
def get_statistics(
    device_id: int,
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    db: Session = Depends(get_db)
):
    """
    Получить статистику по устройству за период.
    
    Возвращает для каждой оси (x, y, z):
    - **min_value**: минимальное значение
    - **max_value**: максимальное значение
    - **count**: количество измерений
    - **sum**: сумма всех значений
    - **median**: медиана
    
    - start_time: опционально, начало периода
    - end_time: опционально, конец периода
    """
    device = crud.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    
    stats = crud.get_device_statistics(db, device_id, start_time, end_time)
    if not stats:
        raise HTTPException(status_code=404, detail="Нет данных для анализа")
    
    return stats