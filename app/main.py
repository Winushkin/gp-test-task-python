from fastapi import FastAPI
from app.database import engine, Base
from app.routers import devices, users, measurments
from fastapi.middleware.cors import CORSMiddleware
from typing import cast

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Statistics Service",
    description="API для сбора и анализа данных с устройств",
    version="1.0.0"
)

app.add_middleware(
    cast(type, CORSMiddleware),
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurments.router, prefix="/api/devices/{device_id}", tags=["measurments"])
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/health")
def health_check():
    """хелсчек сервиса"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)