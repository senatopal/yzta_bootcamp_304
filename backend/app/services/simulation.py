import pandas as pd
from typing import Dict, List, Any

class SimulationService:
    @staticmethod
    def calculate_tariffs(df: pd.DataFrame, consumption_col: str = 'energy(kWh/hh)', price_col: str = 'price_pence') -> Dict[str, float]:
        """
        Calculates total energy consumption and cost in Sterling (£) and pence.
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
        Extracts the top 3 cheapest and most expensive half-hourly time intervals in a day.
        """
        df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            
        df['time_of_day'] = df[timestamp_col].dt.strftime('%H:%M')
        
        # Group by 30-min daily slot and take average price/consumption
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
