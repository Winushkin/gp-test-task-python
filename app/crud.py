from sqlalchemy.orm import Session
from datetime import datetime
import statistics
from app.models import Device, Measurement, User
from app.schemas import DeviceCreate, MeasurementCreate, UserCreate


# Devices
def create_device(db: Session, device: DeviceCreate):
    """Создать новое устройство"""
    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_device_by_name_and_user(db: Session, device: DeviceCreate):
    """Получить устройство по name и user_id"""
    return db.query(Device).filter(Device.name == device.name, Device.user_id == device.user_id).first()


def get_device_by_id(db: Session, device_id: int):
    """Получить устройство по ID"""
    return db.query(Device).filter(Device.id == device_id).first()



def get_all_devices(db: Session):
    """Получить все устройства"""
    return db.query(Device).all()


def delete_device(db: Session, device_id: int):
    """Удалить устройство"""
    device = get_device_by_id(db, device_id)
    if device:
        db.delete(device)
        db.commit()
    return device


# Measurment
def create_measurement(db: Session, device_id: int, measurement: MeasurementCreate):
    """Создать новое измерение для устройства"""
    device = get_device_by_id(db, device_id)
    if not device:
        return None
    
    db_measurement = Measurement(
        device_id=device.id,
        **measurement.model_dump()
    )
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement


def get_measurements_by_device(
    db: Session,
    device_id: int,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """Получить измерения устройства за период (или всё время)"""
    query = db.query(Measurement).join(Device).filter(Device.id == device_id)
    
    if start_time:
        query = query.filter(Measurement.timestamp >= start_time)
    if end_time:
        query = query.filter(Measurement.timestamp <= end_time)
    
    return query.order_by(Measurement.timestamp).all()


# Statistic
def calculate_statistics(values: list):
    """Вычислить статистику для списка значений"""
    if not values:
        return {
            "min_value": 0,
            "max_value": 0,
            "count": 0,
            "sum": 0,
            "median": 0
        }
    
    return {
        "min_value": min(values),
        "max_value": max(values),
        "count": len(values),
        "sum": sum(values),
        "median": statistics.median(values)
    }


def get_device_statistics(
    db: Session,
    device_id: int,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """Получить статистику по устройству"""
    measurements = get_measurements_by_device(db, device_id, start_time, end_time)
    
    if not measurements:
        return None
    
    x_values = [m.x for m in measurements]
    y_values = [m.y for m in measurements]
    z_values = [m.z for m in measurements]
    
    return {
        "device_id": device_id,
        "x_stats": calculate_statistics(x_values),
        "y_stats": calculate_statistics(y_values),
        "z_stats": calculate_statistics(z_values)
    }


# User
def create_user(db: Session, user: UserCreate):
    """Создать нового пользователя"""
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    """Получить пользователя по ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    """Получить всех пользователей"""
    return db.query(User).all()


def get_user_statistics(
    db: Session,
    user_id: int,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """Получить агрегированную статистику по всем устройствам пользователя"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    all_measurements = []
    devices_stats = []
    
    for device in user.devices:
        measurements = get_measurements_by_device(db, device.id, start_time, end_time)
        all_measurements.extend(measurements)
        
        device_stat = get_device_statistics(db, device.id, start_time, end_time)
        if device_stat:
            devices_stats.append(device_stat)
    
    if all_measurements:
        x_values = [m.x for m in all_measurements]
        y_values = [m.y for m in all_measurements]
        z_values = [m.z for m in all_measurements]
        
        aggregated = {
            "x_stats": calculate_statistics(x_values),
            "y_stats": calculate_statistics(y_values),
            "z_stats": calculate_statistics(z_values)
        }
    else:
        aggregated = {
            "x_stats": calculate_statistics([]),
            "y_stats": calculate_statistics([]),
            "z_stats": calculate_statistics([])
        }
    
    return {
        "user_id": user_id,
        "aggregated_stats": aggregated,
        "devices_stats": devices_stats
    }