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


import uvicorn
import os
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db, SessionLocal
from app.models.household import Household

# Endpoint modüllerin
from app.api.endpoints import (
    health,
    households,
    simulation,
    consumption,
    forecast,
    coach,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def quick_seed():
    db = SessionLocal()
    try:
        if db.query(Household).first() is not None:
            return

        base_dir = Path(__file__).resolve().parent.parent
        dataset_dir = os.path.join(base_dir, "dataset")

        if os.path.exists(dataset_dir):
            unique_households = set()
            for file_name in os.listdir(dataset_dir):
                if file_name.endswith(".parquet"):
                    file_path = os.path.join(dataset_dir, file_name)
                    df_ids = pd.read_parquet(file_path, columns=['LCLid'])
                    unique_households.update(df_ids['LCLid'].unique().tolist())
                    del df_ids

            household_objects = [Household(LCLid=lclid) for lclid in unique_households]
            db.bulk_save_objects(household_objects)
            db.commit()
            print("[+] Seed başarıyla tamamlandı.")
    except Exception as e:
        print(f"[!] Seed hatası: {e}")
        db.rollback()
    finally:
        db.close()

quick_seed()


# ==========================================
# FRONTEND UYUMLU HOUSEHOLDS ENDPOINT'LERİ
# ==========================================

@app.get("/households", tags=["Households"])
@app.get(f"{settings.API_V1_STR}/households", tags=["Households"])
def get_household_list(db: Session = Depends(get_db)):
    households = db.query(Household.LCLid).all()
    
    return [h[0] for h in households]


app.include_router(health.router)
app.include_router(households.router, prefix=settings.API_V1_STR)
app.include_router(simulation.router, prefix=settings.API_V1_STR)
app.include_router(consumption.router, prefix=settings.API_V1_STR)
app.include_router(forecast.router, prefix=settings.API_V1_STR)
app.include_router(coach.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)