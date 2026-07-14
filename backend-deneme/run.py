import os
import glob
import pandas as pd
import numpy as np
import uvicorn
from fastapi.testclient import TestClient
from api.main import app
from services.simulation import SimulationService

def run_local_tests():
    print(" Local Parquet veri setleri taranıyor...")
    parquet_files = glob.glob("../dataset/*.parquet")
    
    if not parquet_files:
        parquet_files = glob.glob("dataset/*.parquet")

    if parquet_files:
        target_file = parquet_files[0]
        print(f" Parquet dosyası bulundu ve okunuyor: {target_file}")
        
        df = pd.read_parquet(target_file)
        sample_df = df.head(5000).copy()
        
        if 'tstdropout' in sample_df.columns:
            sample_df['tstp'] = pd.to_datetime(sample_df['tstdropout'], errors='coerce')
        elif 'timestamp' in sample_df.columns:
            sample_df['tstp'] = pd.to_datetime(sample_df['timestamp'], errors='coerce')
            
        if 'energy(kWh)' in sample_df.columns:
            sample_df['energy_kwh'] = pd.to_numeric(sample_df['energy(kWh)'], errors='coerce')
        elif 'hhclean' in sample_df.columns:
            sample_df['energy_kwh'] = pd.to_numeric(sample_df['hhclean'], errors='coerce')
            
        if 'price_pence' not in sample_df.columns:
            sample_df['price_pence'] = np.where(
                (sample_df['tstp'].dt.hour >= 16) & (sample_df['tstp'].dt.hour <= 21), 
                28.5, 
                12.2
            )
            
        sample_df = sample_df.dropna(subset=['tstp', 'energy_kwh'])

        print("\n" + "="*50)
        print(" SIMULATION ENGINE TEST SONUÇLARI ")
        print("="*50)
        cost_results = SimulationService.calculate_tariffs(sample_df)
        print(f" [Görev 1] Toplam Analiz Edilen Tüketim : {cost_results['total_consumption_kwh']} kWh")
        print(f" [Görev 1] Hesaplanan Toplam Maliyet   : £{cost_results['total_cost_pounds']}")
        print("-" * 50)
        
        hour_results = SimulationService.analyze_critical_hours(sample_df)
        print(" [Görev 2] EN UCUZ 3 ZAMAN DİLİMİ:")
        for slot in hour_results['cheapest_hours']:
            print(f"    Saat: {slot['time_slot']} | Ort. Fiyat: {slot['avg_price_pence']}p")
        print("="*50)

        print("\n API ENDPOINT TESTLERİ BAŞLIYOR ")
        client = TestClient(app)
        
        test_records = sample_df[['tstp', 'energy_kwh', 'price_pence']].head(50).copy()
        test_records['tstp'] = test_records['tstp'].dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        api_payload = {
            "household_id": "MAC000002",
            "data": test_records.to_dict(orient='records')
        }
        
        res_costs = client.post("/api/v1/simulation/costs", json=api_payload)
        print(f"-> /costs Endpoint Durumu: {res_costs.status_code}")
        
        res_hours = client.post("/api/v1/simulation/hours", json=api_payload)
        print(f"-> /hours Endpoint Durumu: {res_hours.status_code}")
        print("="*50 + "\n")

    else:
        print(" HATA: 'dataset' klasörü altında .parquet dosyası bulunamadı!")

if __name__ == "__main__":
    run_local_tests()
    
    print(" API Sunucusu başlatılıyor...")
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)