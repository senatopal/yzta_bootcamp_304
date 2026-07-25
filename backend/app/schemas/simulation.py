from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Any

class HouseholdConsumptionInput(BaseModel):
    tstp: datetime
    energy_kwh: float = Field(..., alias="energy(kWh/hh)", ge=0) 
    price_pence: float = Field(..., ge=0)

    class Config:
        populate_by_name = True

class SimulationRequest(BaseModel):
    household_id: str
    data: List[HouseholdConsumptionInput]
    devices: Optional[Dict[str, Dict[str, float]]] = None

class CarbonImpactDetail(BaseModel):
    energy_kwh: float
    emission_factor_kg_per_kwh: float
    carbon_kg: float

class SimulationCostResponse(BaseModel):
    household_id: str
    total_consumption_kwh: float
    total_cost_pounds: float
    total_cost_pence: float
    carbon_impact: Optional[CarbonImpactDetail] = None
    message: str

class TimeSlotDetail(BaseModel):
    time_slot: str
    avg_price_pence: float
    avg_consumption_kwh: float

class SimulationHoursResponse(BaseModel):
    household_id: str
    cheapest_hours: List[TimeSlotDetail]
    expensive_hours: List[TimeSlotDetail]

class LoadShiftRecommendationDetail(BaseModel):
    device: str
    icon: str
    current_hour: str
    recommended_hour: str
    estimated_savings_pounds: float
    saving_percent: float
    carbon_reduction_kg: float
    message: str

class LoadShiftResponse(BaseModel):
    household_id: str
    expensive_hour: str
    recommended_hour: str
    total_savings_pounds: float
    recommendations: List[LoadShiftRecommendationDetail]

class AnomalyDetail(BaseModel):
    timestamp: str
    expected_kwh: float
    actual_kwh: float
    deviation_percent: float
    message: str

class AnomalyResponse(BaseModel):
    household_id: str
    anomaly_detected: bool
    anomali_var: bool
    anomalies: List[AnomalyDetail]
    saat: Optional[str] = None
    beklenen_kwh: Optional[float] = None
    gerceklesen_kwh: Optional[float] = None
    sapma_yuzde: float
    message: str

