from fastapi import APIRouter, HTTPException
import pandas as pd
from app.schemas.simulation import (
    SimulationRequest,
    SimulationCostResponse,
    SimulationHoursResponse,
    LoadShiftResponse,
    AnomalyResponse
)
from app.services.simulation import SimulationService

router = APIRouter()

@router.post(
    "/simulation/costs", 
    response_model=SimulationCostResponse, 
    tags=["Simulation"]
)
async def calculate_household_costs(payload: SimulationRequest):
    """
    Simulates electricity costs across standard vs dynamic time-of-use tariffs.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Data payload cannot be empty.")
    
    # Load input records into DataFrame
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    metrics = SimulationService.calculate_tariffs(
        df, 
        consumption_col='energy(kWh/hh)', 
        price_col='price_pence'
    )
    
    return {
        "household_id": payload.household_id,
        **metrics,
        "carbon_impact": SimulationService.calculate_carbon_impact(metrics["total_consumption_kwh"]),
        "message": "Cost simulation completed successfully."
    }

@router.post(
    "/simulation/hours", 
    response_model=SimulationHoursResponse, 
    tags=["Simulation"]
)
async def analyze_peak_hours(payload: SimulationRequest):
    """
    Analyzes daily peak loads and identifies the top 3 cheapest and most expensive time intervals.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Data payload cannot be empty.")
        
    # Load input records into DataFrame
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    analysis_results = SimulationService.analyze_critical_hours(
        df, 
        timestamp_col='tstp', 
        consumption_col='energy(kWh/hh)', 
        price_col='price_pence'
    )
    
    return {
        "household_id": payload.household_id,
        **analysis_results
    }

@router.post(
    "/recommendations/load-shift",
    response_model=LoadShiftResponse,
    tags=["Simulation"]
)
async def load_shift_recommendations(payload: SimulationRequest):
    """
    Recommends optimal times to shift appliance loads to minimize dynamic tariff costs.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Data payload cannot be empty.")
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    return SimulationService.generate_load_shift_recommendations(
        df, 
        payload.household_id, 
        payload.devices
    )

@router.post(
    "/alerts/anomaly",
    response_model=AnomalyResponse,
    tags=["Simulation"]
)
async def anomaly_alert(payload: SimulationRequest):
    """
    Checks consumption against historical averages to detect abnormal peaks or potential waste.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Data payload cannot be empty.")
    df = pd.DataFrame([item.model_dump(by_alias=True) for item in payload.data])
    return SimulationService.detect_anomaly(df, payload.household_id)
