import pandas as pd
from typing import Dict, List, Any

class SimulationService:
    UK_GRID_EMISSION_FACTOR_KG_PER_KWH = 0.193
    DEFAULT_DEVICES = {
        "Çamaşır Makinesi": {"power_kw": 0.5, "duration_hours": 1.0, "icon": "👕"},
        "Bulaşık Makinesi": {"power_kw": 1.2, "duration_hours": 1.5, "icon": "🍽️"},
        "Kurutma Makinesi": {"power_kw": 2.0, "duration_hours": 1.0, "icon": "🌀"},
        "Elektrikli Araç Şarjı": {"power_kw": 3.6, "duration_hours": 1.0, "icon": "🔌"},
    }

    @staticmethod
    def calculate_tariffs(df: pd.DataFrame, consumption_col: str = 'energy(kWh/hh)', price_col: str = 'price_pence') -> Dict[str, float]:
        """
        Yarım saatlik tüketim maliyetini sterlin (£) cinsinden hesaplar.
        """
        df = df.copy()
        df['cost_pence'] = df[consumption_col] * df[price_col]
        
        total_pence = df['cost_pence'].sum()
        total_pounds = round(total_pence / 100, 2)
        total_consumption_kwh = round(df[consumption_col].sum(), 2)
        
        return {
            "total_consumption_kwh": total_consumption_kwh,
            "total_cost_pounds": total_pounds,
            "total_cost_pence": round(total_pence, 2)
        }

    @staticmethod
    def analyze_critical_hours(df: pd.DataFrame, timestamp_col: str = 'tstp', consumption_col: str = 'energy(kWh/hh)', price_col: str = 'price_pence') -> Dict[str, List[Dict[str, Any]]]:
        """
        Günün en ucuz ve en pahalı 3 zaman dilimini listeler.
        """
        df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            
        df['time_of_day'] = df[timestamp_col].dt.strftime('%H:%M')
        
        hourly_summary = df.groupby('time_of_day').agg(
            avg_price_pence=(price_col, 'mean'),
            avg_consumption=(consumption_col, 'mean')
        ).reset_index()
        
        cheapest_slots = hourly_summary.sort_values(by='avg_price_pence', ascending=True).head(3)
        expensive_slots = hourly_summary.sort_values(by='avg_price_pence', ascending=False).head(3)
        
        return {
            "cheapest_hours": [
                {
                    "time_slot": r['time_of_day'], 
                    "avg_price_pence": round(r['avg_price_pence'], 2), 
                    "avg_consumption_kwh": round(r['avg_consumption'], 3)
                } 
                for _, r in cheapest_slots.iterrows()
            ],
            "expensive_hours": [
                {
                    "time_slot": r['time_of_day'], 
                    "avg_price_pence": round(r['avg_price_pence'], 2), 
                    "avg_consumption_kwh": round(r['avg_consumption'], 3)
                } 
                for _, r in expensive_slots.iterrows()
            ]
        }

    @staticmethod
    def calculate_carbon_impact(energy_kwh: float, emission_factor_kg_per_kwh: float = UK_GRID_EMISSION_FACTOR_KG_PER_KWH) -> Dict[str, float]:
        """Enerjinin şebeke emisyon karşılığını kg CO2 olarak verir."""
        energy_kwh = max(float(energy_kwh), 0.0)
        return {
            "energy_kwh": round(energy_kwh, 3),
            "emission_factor_kg_per_kwh": emission_factor_kg_per_kwh,
            "carbon_kg": round(energy_kwh * emission_factor_kg_per_kwh, 3),
        }

    @staticmethod
    def generate_load_shift_recommendations(df: pd.DataFrame, household_id: str, devices: Dict[str, Dict[str, float]] = None, top_n: int = 4) -> Dict[str, Any]:
        """Pahalı gözlemleri en ucuz saatlere kaydırarak cihaz bazında tasarruf önerir."""
        data = df.copy()
        data['timestamp'] = pd.to_datetime(data['tstp'])
        data['hour'] = data['timestamp'].dt.strftime('%H:%M')
        prices = data.groupby('hour')['price_pence'].mean()
        if prices.empty:
            return {"household_id": household_id, "recommendations": [], "total_savings_pounds": 0.0}
        expensive_hour, cheapest_hour = str(prices.idxmax()), str(prices.idxmin())
        expensive_price, cheapest_price = float(prices.max()), float(prices.min())
        recommendations = []
        for device, profile in (devices or SimulationService.DEFAULT_DEVICES).items():
            energy = float(profile.get('power_kw', 1.0)) * float(profile.get('duration_hours', 1.0))
            saving_pounds = max(energy * (expensive_price - cheapest_price) / 100, 0.0)
            carbon = SimulationService.calculate_carbon_impact(energy * 0.25)
            reduction_percent = saving_pounds / (energy * expensive_price / 100) * 100 if expensive_price else 0.0
            recommendations.append({
                "device": device, "icon": profile.get('icon', '⚡'), "current_hour": expensive_hour,
                "recommended_hour": cheapest_hour, "estimated_savings_pounds": round(saving_pounds, 2),
                "saving_percent": round(reduction_percent, 1), "carbon_reduction_kg": carbon['carbon_kg'],
                "message": f"{device} cihazını {expensive_hour} yerine {cheapest_hour} saatinde çalıştırırsan £{saving_pounds:.2f} tasarruf edebilirsin.",
            })
        recommendations.sort(key=lambda item: item['estimated_savings_pounds'], reverse=True)
        return {
            "household_id": household_id, "expensive_hour": expensive_hour, "recommended_hour": cheapest_hour,
            "total_savings_pounds": round(sum(item['estimated_savings_pounds'] for item in recommendations), 2),
            "recommendations": recommendations[:top_n],
        }

    @staticmethod
    def detect_anomaly(df: pd.DataFrame, household_id: str, threshold_std: float = 3.0) -> Dict[str, Any]:
        """Aynı saat ortalamasından 3 sigma veya 3 kat fazla tüketimleri işaretler."""
        data = df.copy()
        data['timestamp'] = pd.to_datetime(data['tstp'])
        data['time_of_day'] = data['timestamp'].dt.strftime('%H:%M')
        grouped = data.groupby('time_of_day')['energy(kWh/hh)']
        baseline, std = grouped.transform('mean'), grouped.transform('std').fillna(0)
        global_median = float(data['energy(kWh/hh)'].median())
        sample_count = grouped.transform('count')
        baseline = baseline.where(sample_count >= 3, global_median)
        ratio = data['energy(kWh/hh)'] / baseline.replace(0, pd.NA)
        z_score = (data['energy(kWh/hh)'] - baseline) / std.replace(0, pd.NA)
        flagged = ((ratio >= 3.0) | (z_score >= threshold_std)).fillna(False)
        anomalies = []
        for index in data.index[flagged]:
            row, expected, actual = data.loc[index], float(baseline.loc[index]), float(data.loc[index, 'energy(kWh/hh)'])
            anomalies.append({
                "timestamp": row['timestamp'].isoformat(), "expected_kwh": round(expected, 3), "actual_kwh": round(actual, 3),
                "deviation_percent": round((actual - expected) / expected * 100, 1) if expected else 0.0,
                "message": "Açık unutulmuş cihaz veya olası bir israf tespit edildi.",
            })
        first = anomalies[0] if anomalies else None
        return {
            "household_id": household_id, "anomaly_detected": bool(anomalies), "anomali_var": bool(anomalies),
            "anomalies": anomalies,
            "saat": first["timestamp"] if first else None,
            "beklenen_kwh": first["expected_kwh"] if first else None,
            "gerceklesen_kwh": first["actual_kwh"] if first else None,
            "sapma_yuzde": first["deviation_percent"] if first else 0.0,
            "message": first['message'] if first else "Tüketim deseni normal görünüyor.",
        }