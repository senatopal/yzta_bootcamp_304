from pydantic import BaseModel
from typing import List

class ConsumptionHistoryPoint(BaseModel):
    timestamp: str
    consumption_kwh: float
    cost_pounds: float
    avg_price_pence: float

class ConsumptionHistoryResponse(BaseModel):
    household_id: str
    period: str
    data: List[ConsumptionHistoryPoint]
