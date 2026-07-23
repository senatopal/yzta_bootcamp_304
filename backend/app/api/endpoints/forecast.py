from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.models.consumption import ConsumptionReading
from app.schemas.forecast import ForecastResponse
from app.services.forecast import ForecastService

router = APIRouter()

@router.get(
    "/consumption/forecast",
    response_model=ForecastResponse,
    tags=["Consumption"]
)
def get_consumption_forecast(
    household_id: str = Query(..., description="LCLid of the household"),
    days: int = Query(1, ge=1, le=7, description="Number of days to forecast (1-7)"),
    start_date: Optional[datetime] = Query(None, description="Start date of forecast (ISO format). Defaults to the time after latest database reading."),
    db: Session = Depends(get_db)
):
    """
    Returns electricity consumption forecast for the specified household.
    Uses Yasemin's ML model (if saved_models/forecast_model.pkl exists) or falls back
    to historical averages for this household.
    """
    # Determine start date if not provided
    if start_date is None:
        latest_reading = db.query(ConsumptionReading.tstp)\
            .filter(ConsumptionReading.LCLid == household_id)\
            .order_by(ConsumptionReading.tstp.desc())\
            .first()
            
        if latest_reading:
            start_date = latest_reading[0] + timedelta(minutes=30)
        else:
            start_date = datetime.now()

    # Get forecast
    try:
        data_points = ForecastService.predict_consumption(
            db=db,
            household_id=household_id,
            start_date=start_date,
            forecast_days=days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

    return ForecastResponse(
        household_id=household_id,
        forecast_days=days,
        data=data_points
    )
