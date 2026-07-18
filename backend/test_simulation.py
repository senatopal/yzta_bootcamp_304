import os
import sys
import glob
import pandas as pd
import uvicorn
from fastapi.testclient import TestClient

# Put current backend dir in path for local import
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from app.services.simulation import SimulationService

def run_local_tests():
    print("=== Volti Integration & Simulation Tests ===")
    
    # Locate dataset path (matches project root layout)
    parquet_files = (
        glob.glob("dataset/*.parquet") + 
        glob.glob("../dataset/*.parquet") +
        glob.glob("../../dataset/*.parquet")
    )
    
    if not parquet_files:
        print("[!] Warning: No parquet files found in 'dataset/'. Cannot run calculations check.")
        print("    Please run data preparation notebook first to export Parquet blocks.")
        return
        
    target_file = parquet_files[0]
    print(f"[*] Reading sample from Parquet file: {target_file}")
    
    df = pd.read_parquet(target_file)
    sample_df = df.head(5000).copy()
    
    # Clean up fields
    cols_to_clean = [col for col in ['tstp', 'energy(kWh/hh)', 'price_pence'] if col in sample_df.columns]
    if cols_to_clean:
        sample_df = sample_df.dropna(subset=cols_to_clean)
        
    print(f"[*] Preprocessing complete. DataFrame Columns: {list(sample_df.columns)}")
    
    # 1. Test Simulation Service calculations
    print("\n" + "="*50)
    print(" VOLTI SIMULATION SERVICE VERIFICATION ")
    print("="*50)
    cost_results = SimulationService.calculate_tariffs(sample_df, consumption_col='energy(kWh/hh)')
    print(f" Total Consumption Modeled   : {cost_results['total_consumption_kwh']:,} kWh")
    print(f" Calculated Tariff Cost      : £{cost_results['total_cost_pounds']:,}")
    print("-" * 50)
    
    hour_results = SimulationService.analyze_critical_hours(sample_df, consumption_col='energy(kWh/hh)')
    print(" TOP 3 MOST EXPENSIVE (PEAK) SLOTS:")
    for slot in hour_results['expensive_hours']:
        print(f"    Slot: {slot['time_slot']} | Avg Price: {slot['avg_price_pence']}p")
    print("="*50)

    # 2. Test FastAPI Integration
    print("\n FASTAPI INTEGRATION TEST (TESTCLIENT) ")
    client = TestClient(app)
    
    # Prepare payload orienting records
    test_records = sample_df[['tstp', 'energy(kWh/hh)', 'price_pence']].head(50).copy()
    test_records['tstp'] = test_records['tstp'].dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    api_payload = {
        "household_id": "MAC000002",
        "data": test_records.to_dict(orient='records')
    }
    
    # Post cost simulation
    res_costs = client.post("/api/v1/simulation/costs", json=api_payload)
    print(f"-> POST /api/v1/simulation/costs: {res_costs.status_code} ({'OK' if res_costs.status_code == 200 else 'FAILED'})")
    if res_costs.status_code == 200:
        print(f"   Response Preview: {res_costs.json()}")
        
    # Post peak hours analysis
    res_hours = client.post("/api/v1/simulation/hours", json=api_payload)
    print(f"-> POST /api/v1/simulation/hours: {res_hours.status_code} ({'OK' if res_hours.status_code == 200 else 'FAILED'})")
    if res_hours.status_code == 200:
        print(f"   Cheapest Slots: {[s['time_slot'] for s in res_hours.json()['cheapest_hours']]}")
        
    print("="*50 + "\n")

if __name__ == "__main__":
    run_local_tests()
