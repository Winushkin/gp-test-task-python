from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DeviceCreate, DeviceResponse
from app import crud

router = APIRouter()


# Devices
@router.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """
    Создать новое устройство.
    
    - **name**: название устройства
    - user_id: опционально, ID пользователя-владельца
    """
    existing = crud.get_device_by_name_and_user(db, device)
    if existing:
        raise HTTPException(status_code=400, detail="Устройство с таким ID уже существует")
    
    return crud.create_device(db, device)


@router.get("/", response_model=list[DeviceResponse])
def get_devices(db: Session = Depends(get_db)):
    """Получить список всех устройств"""
    return crud.get_all_devices(db)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретном устройстве"""
    device = crud.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return device


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Удалить устройство"""
    device = crud.delete_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return {"message": "Устройство удалено"}
