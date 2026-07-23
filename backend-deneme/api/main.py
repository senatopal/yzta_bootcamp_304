from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from services.simulation import SimulationService

app = FastAPI(title="Volti Simulation API")

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

@app.post("/api/v1/simulation/costs")
async def calculate_household_costs(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
    
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    metrics = SimulationService.calculate_tariffs(df, consumption_col='energy(kWh/hh)', price_col='price_pence')
    
    return {
        "household_id": payload.household_id,
        **metrics,
        "carbon_impact": SimulationService.calculate_carbon_impact(metrics["total_consumption_kwh"]),
        "message": "Maliyet simülasyonu tamamlandı."
    }

@app.post("/api/v1/simulation/hours")
async def analyze_peak_hours(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
        
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    analysis_results = SimulationService.analyze_critical_hours(df, timestamp_col='tstp', consumption_col='energy(kWh/hh)', price_col='price_pence')
    
    return {
        "household_id": payload.household_id,
        **analysis_results
    }

@app.post("/api/v1/recommendations/load-shift")
async def load_shift_recommendations(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    return SimulationService.generate_load_shift_recommendations(df, payload.household_id, payload.devices)

@app.post("/api/v1/alerts/anomaly")
async def anomaly_alert(payload: SimulationRequest):
    if not payload.data:
        raise HTTPException(status_code=400, detail="Veri listesi boş olamaz.")
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    return SimulationService.detect_anomaly(df, payload.household_id)