from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.simulation import (
    TimeSlotDetail,
    LoadShiftRecommendationDetail,
    AnomalyDetail
)

class WeeklySummaryDetail(BaseModel):
    start_date: datetime
    end_date: datetime
    total_consumption_kwh: float
    total_cost_pounds: float
    average_price_pence: float

class CoachContextResponse(BaseModel):
    household_id: str
    weekly_summary: Optional[WeeklySummaryDetail] = None
    cheapest_hours: List[TimeSlotDetail]
    expensive_hours: List[TimeSlotDetail]
    recommendations: List[LoadShiftRecommendationDetail]
    anomalies: List[AnomalyDetail]
    prompt_context: str
