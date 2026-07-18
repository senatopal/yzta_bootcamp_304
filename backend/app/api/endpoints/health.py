from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.health import HealthCheck
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthCheck, tags=["System Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Check server status and verify database connectivity.
    """
    db_status = "unhealthy"
    try:
        # Test query to check if connection is active
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        print(f"[!] Database connection check failed: {e}")
        db_status = f"unhealthy: {type(e).__name__}"
        
    return {
        "status": "ok",
        "database": db_status,
        "project_name": settings.PROJECT_NAME
    }
