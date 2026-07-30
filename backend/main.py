# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# from app.core.database import engine, Base
# from app.api.endpoints import health, households, simulation, consumption, forecast, coach

# # Initialize database tables automatically at startup
# try:
#     Base.metadata.create_all(bind=engine)
# except Exception as e:
#     print(f"[!] Warning: Could not automatically create database tables: {e}")


# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # Set CORS origins (allows Sena's React/Next.js frontend to query API)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust for production origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Register endpoints
# app.include_router(health.router)
# app.include_router(households.router, prefix=settings.API_V1_STR)
# app.include_router(simulation.router, prefix=settings.API_V1_STR)
# app.include_router(consumption.router, prefix=settings.API_V1_STR)
# app.include_router(forecast.router, prefix=settings.API_V1_STR)
# app.include_router(coach.router, prefix=settings.API_V1_STR)

# if __name__ == "__main__":
#     # Start web server on port 8000
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db, Base, engine

app = FastAPI(
    title="Energy Consumption Analytics API",
    description="PostgreSQL (Neon) ve FastAPI tabanlı enerji tüketim analizi backend servisi.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Energy Consumption API çalışıyor.",
        "docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        
        households_count = db.execute(text("SELECT COUNT(*) FROM households")).scalar()
        records_count = db.execute(text("SELECT COUNT(*) FROM consumption_records")).scalar()
        
        return {
            "database": "connected",
            "households_count": households_count,
            "consumption_records_count": records_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Veritabanı bağlantı hatası: {str(e)}"
        )