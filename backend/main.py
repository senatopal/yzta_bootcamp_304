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
from pathlib import Path
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn

from app.api.endpoints import (
    coach,
    consumption,
    forecast,
    health,
    households,
    simulation,
)
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine, get_db
from app.models.household import Household

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
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
            print("[i] Household tablosunda veri zaten mevcut, seed atlandı.")
            return

        unique_households = set()

        try:
            result = db.execute(
                text('SELECT DISTINCT "LCLid" FROM consumption_records;')
            )
            db_ids = [row[0] for row in result.fetchall() if row[0]]
            if db_ids:
                unique_households.update(db_ids)
                print(
                    f"[*] Neon 'consumption_records' tablosundan {len(db_ids)} ev bulundu."
                )
        except Exception as db_err:
            print(
                f"[!] Veritabanından LCLid okunurken hata/tablo yok: {db_err}"
            )

        if not unique_households:
            BASE_DIR = Path(__file__).resolve().parent
            dataset_dir = BASE_DIR.parent / "dataset"
            if not dataset_dir.exists():
                dataset_dir = BASE_DIR.parent.parent / "dataset"

            if dataset_dir.exists():
                parquet_files = sorted(dataset_dir.glob("*.parquet"))
                if parquet_files:
                    sample_file = parquet_files[0]
                    print(
                        f"[*] Dosyadan okunuyor: {sample_file.name}..."
                    )
                    df_ids = pd.read_parquet(sample_file, columns=["LCLid"])
                    unique_households.update(df_ids["LCLid"].unique().tolist())
                    del df_ids

        if unique_households:
            household_objects = [
                Household(LCLid=lclid) for lclid in unique_households
            ]
            db.bulk_save_objects(household_objects)
            db.commit()
            print(
                f"[+] {len(household_objects)} adet ev (LCLid) başarıyla 'Household' tablosuna eklendi."
            )
        else:
            print("[!] Hiçbir LCLid kaynağı bulunamadı.")

    except Exception as e:
        print(f"[!] Seed genel hatası: {e}")
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