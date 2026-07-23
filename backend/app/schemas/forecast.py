from pydantic import BaseModel
from typing import List

class ForecastDataPoint(BaseModel):
    timestamp: str
    predicted_kwh: float

class ForecastResponse(BaseModel):
    household_id: str
    forecast_days: int
    data: List[ForecastDataPoint]
