from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class HouseholdConsumptionInput(BaseModel):
    tstp: datetime
    energy_kwh: float = Field(..., alias="energy(kWh/hh)", ge=0) 
    price_pence: float = Field(..., ge=0)

    class Config:
        populate_by_name = True

class SimulationRequest(BaseModel):
    household_id: str
    data: List[HouseholdConsumptionInput]

class SimulationCostResponse(BaseModel):
    household_id: str
    total_consumption_kwh: float
    total_cost_pounds: float
    total_cost_pence: float
    message: str

class TimeSlotDetail(BaseModel):
    time_slot: str
    avg_price_pence: float
    avg_consumption_kwh: float

class SimulationHoursResponse(BaseModel):
    household_id: str
    cheapest_hours: List[TimeSlotDetail]
    expensive_hours: List[TimeSlotDetail]
