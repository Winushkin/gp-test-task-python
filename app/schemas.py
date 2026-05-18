from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Measurement
class MeasurementBase(BaseModel):
    """Базовая схема измерения"""
    x: float
    y: float
    z: float

class MeasurementCreate(MeasurementBase):
    """Схема для создания измерения"""
    pass

class MeasurementResponse(MeasurementBase):
    """Схема ответа с измерением"""
    id: int
    device_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Statistics
class StatisticsResponse(BaseModel):
    """Результаты анализа данных"""
    min_value: float
    max_value: float
    count: int
    sum: float
    median: float


class DeviceStatisticsResponse(BaseModel):
    """Статистика по конкретному устройству"""
    device_id: int
    x_stats: StatisticsResponse
    y_stats: StatisticsResponse
    z_stats: StatisticsResponse


# Device
class DeviceBase(BaseModel):
    """Базовая схема устройства"""
    name: str

class DeviceCreate(DeviceBase):
    """Схема для создания устройства"""
    user_id: Optional[int] = None

class DeviceResponse(DeviceBase):
    """Схема ответа с информацией об устройстве"""
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


# User
class UserBase(BaseModel):
    """Базовая схема пользователя"""
    name: str
    email: str

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    pass

class UserResponse(UserBase):
    """Схема ответа с информацией о пользователе"""
    id: int
    devices: List[DeviceResponse] = []

    class Config:
        from_attributes = True

class AggregatedAxesStats(BaseModel):
    """Метрики, разделенные по трем осям координат"""
    x_stats: StatisticsResponse
    y_stats: StatisticsResponse
    z_stats: StatisticsResponse


class UserStatisticsResponse(BaseModel):
    """Агрегированная статистика по всем устройствам пользователя"""
    user_id: int
    aggregated_stats: AggregatedAxesStats 
    devices_stats: List[DeviceStatisticsResponse] = Field(default_factory=list)
