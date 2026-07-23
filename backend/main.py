import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.endpoints import health, households, simulation, consumption, forecast

# Initialize database tables automatically if using SQLite fallback
if settings.DATABASE_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set CORS origins (allows Sena's React/Next.js frontend to query API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(health.router)
app.include_router(households.router, prefix=settings.API_V1_STR)
app.include_router(simulation.router, prefix=settings.API_V1_STR)
app.include_router(consumption.router, prefix=settings.API_V1_STR)
app.include_router(forecast.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # Start web server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
