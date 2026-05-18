from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    """Модель пользователя - опционально"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    devices = relationship("Device", back_populates="user")


class Device(Base):
    """Модель устройства"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Опционально
    
    user = relationship("User", back_populates="devices")
    measurements = relationship("Measurement", back_populates="device", cascade="all, delete-orphan")


class Measurement(Base):
    """Модель измерения (x, y, z с временной меткой)"""
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))    
    
    device = relationship("Device", back_populates="measurements")