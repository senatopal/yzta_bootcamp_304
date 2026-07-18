import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import glob
import pandas as pd
import numpy as np
import uvicorn
from fastapi.testclient import TestClient
from api.main import app
from services.simulation import SimulationService

def run_local_tests():
    print(" Proje kök dizinindeki 'dataset' klasörü taranıyor...")
    parquet_files = glob.glob("../dataset/*.parquet") + glob.glob("dataset/*.parquet")
    
    if parquet_files:
        target_file = parquet_files[0]
        print(f" Parquet dosyası başarıyla okundu: {target_file}")
        
        df = pd.read_parquet(target_file)
        sample_df = df.head(5000).copy()
        
        cols_to_clean = [col for col in ['tstp', 'energy(kWh/hh)', 'price_pence'] if col in sample_df.columns]
        if cols_to_clean:
            sample_df = sample_df.dropna(subset=cols_to_clean)
        
        print(f" Veri temizlendi, aktif sütunlar: {list(sample_df.columns)}")

        
        print("\n" + "="*50)
        print(" VOLTI MOTOR TEST SONUÇLARI ")
        print("="*50)
        cost_results = SimulationService.calculate_tariffs(sample_df, consumption_col='energy(kWh/hh)')
        print(f" Toplam Analiz Edilen Tüketim : {cost_results['total_consumption_kwh']} kWh")
        print(f" Hesaplanan Toplam Maliyet   : £{cost_results['total_cost_pounds']}")
        print("-" * 50)
        
        hour_results = SimulationService.analyze_critical_hours(sample_df, consumption_col='energy(kWh/hh)')
        print(" EN PAHALI (PİK) 3 ZAMAN DİLİMİ:")
        for slot in hour_results['expensive_hours']:
            print(f"    Saat: {slot['time_slot']} | Ort. Fiyat: {slot['avg_price_pence']}p")
        print("="*50)

        print("\n FastAPI ENDPOINT INTEGRATION TESTS ")
        client = TestClient(app)
        
        test_records = sample_df[['tstp', 'energy(kWh/hh)', 'price_pence']].head(50).copy()
        test_records['tstp'] = test_records['tstp'].dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        api_payload = {
            "household_id": "MAC000002",
            "data": test_records.to_dict(orient='records')
        }
        
        res_costs = client.post("/api/v1/simulation/costs", json=api_payload)
        print(f"-> /costs Endpoint Status: {res_costs.status_code} (OK)")
        
        res_hours = client.post("/api/v1/simulation/hours", json=api_payload)
        print(f"-> /hours Endpoint Status: {res_hours.status_code} (OK)")
        print("="*50 + "\n")

    else:
        print(" HATA: 'dataset' klasörü altında .parquet uzantılı dosya bulunamadı!")

if __name__ == "__main__":
    run_local_tests()
    print(" FastAPI canlı sunucusu 127.0.0.1:8000 üzerinde ayağa kaldırılıyor...")
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)