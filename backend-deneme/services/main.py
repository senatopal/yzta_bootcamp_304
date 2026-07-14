from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import pandas as pd
from services.simulation import SimulationService

app = FastAPI(title="Volti Simulation API")

class HouseholdConsumptionInput(BaseModel):
    tstp: datetime
    energy_kwh: float = Field(..., ge=0)
    price_pence: float = Field(..., ge=0)

class SimulationRequest(BaseModel):
    household_id: str
    data: List[HouseholdConsumptionInput]

@app.post("/api/v1/simulation/costs")
async def calculate_household_costs(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
    
    df = pd.DataFrame([item.model_dump() for item in payload.data])
    metrics = SimulationService.calculate_tariffs(df, consumption_col='energy_kwh', price_col='price_pence')
    
    return {
        "household_id": payload.household_id,
        **metrics,
        "message": "Maliyet simülasyonu tamamlandı."
    }

@app.post("/api/v1/simulation/hours")
async def analyze_peak_hours(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
        
    df = pd.DataFrame([item.model_dump() for item in payload.data])
    analysis_results = SimulationService.analyze_critical_hours(df, timestamp_col='tstp', consumption_col='energy_kwh', price_col='price_pence')
    
    return {
        "household_id": payload.household_id,
        **analysis_results
    }