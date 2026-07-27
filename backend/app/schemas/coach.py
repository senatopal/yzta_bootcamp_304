from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from typing import Literal
from pydantic import Field
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


class CoachChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)


class CoachChatRequest(BaseModel):
    household_id: str
    message: str = Field(min_length=1, max_length=2000)
    history: List[CoachChatMessage] = Field(default_factory=list)


class CoachChatResponse(BaseModel):
    household_id: str
    answer: str
    model: str
    response_id: Optional[str] = None
    grounded: bool = True