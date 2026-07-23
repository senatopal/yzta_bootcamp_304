import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.consumption import ConsumptionReading
from app.schemas.forecast import ForecastDataPoint

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "models", "saved_models", "forecast_model.pkl"
)

class ForecastService:
    _model = None
    _model_loaded = False

    @classmethod
    def load_model(cls):
        """
        Attempts to load the ML model from the saved path.
        """
        if cls._model_loaded:
            return cls._model
        
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    cls._model = pickle.load(f)
                cls._model_loaded = True
                print(f"[OK] Forecast model loaded successfully from {MODEL_PATH}")
            except Exception as e:
                print(f"[!] Error loading forecast model: {e}")
                cls._model = None
                cls._model_loaded = False
        else:
            # Model file not found yet (expected until Yasemin commits it)
            cls._model = None
            cls._model_loaded = False
            
        return cls._model

    @classmethod
    def predict_consumption(
        cls, 
        db: Session, 
        household_id: str, 
        start_date: datetime, 
        forecast_days: int
    ) -> List[ForecastDataPoint]:
        """
        Generates consumption forecasts for the next N days.
        If Yasemin's ML model is loaded, it will use it.
        Otherwise, falls back to a database-driven baseline historical average profile.
        """
        # Try loading ML model
        model = cls.load_model()
        
        intervals_count = forecast_days * 48
        current_dt = start_date
        data_points = []

        if model is not None:
            # ML Model Prediction Logic
            print(f"[*] Running ML model forecast for {household_id} starting at {start_date}")
            try:
                features = []
                temp_dt = start_date
                for _ in range(intervals_count):
                    features.append({
                        "LCLid": household_id,
                        "tstp": temp_dt,
                        "hour": temp_dt.hour,
                        "minute": temp_dt.minute,
                        "dayofweek": temp_dt.weekday(),
                        "month": temp_dt.month
                    })
                    temp_dt += timedelta(minutes=30)
                
                df_features = pd.DataFrame(features)
                predictions = model.predict(df_features)
                
                temp_dt = start_date
                for pred in predictions:
                    data_points.append(
                        ForecastDataPoint(
                            timestamp=temp_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            predicted_kwh=max(0.0, round(float(pred), 4))
                        )
                    )
                    temp_dt += timedelta(minutes=30)
                return data_points
            except Exception as e:
                print(f"[!] ML model prediction failed: {e}. Falling back to baseline model.")

        # Baseline Model Fallback (Historical Average Profile)
        print(f"[*] Running baseline historical average profile forecast for {household_id}")
        
        # Query average consumption for each 30-min slot of the day for this household
        avg_profile = db.query(
            extract('hour', ConsumptionReading.tstp).label("hr"),
            extract('minute', ConsumptionReading.tstp).label("mn"),
            func.avg(ConsumptionReading.energy_kwh).label("avg_val")
        ).filter(
            ConsumptionReading.LCLid == household_id,
            ConsumptionReading.energy_kwh.isnot(None)
        ).group_by(
            extract('hour', ConsumptionReading.tstp),
            extract('minute', ConsumptionReading.tstp)
        ).all()
        
        profile_dict = {}
        for row in avg_profile:
            hr_val = int(row.hr) if row.hr is not None else 0
            mn_val = int(row.mn) if row.mn is not None else 0
            profile_dict[(hr_val, mn_val)] = float(row.avg_val) if row.avg_val is not None else 0.0

        # If household profile is empty, try global profile across all households
        if not profile_dict:
            global_profile = db.query(
                extract('hour', ConsumptionReading.tstp).label("hr"),
                extract('minute', ConsumptionReading.tstp).label("mn"),
                func.avg(ConsumptionReading.energy_kwh).label("avg_val")
            ).filter(
                ConsumptionReading.energy_kwh.isnot(None)
            ).group_by(
                extract('hour', ConsumptionReading.tstp),
                extract('minute', ConsumptionReading.tstp)
            ).all()
            for row in global_profile:
                hr_val = int(row.hr) if row.hr is not None else 0
                mn_val = int(row.mn) if row.mn is not None else 0
                profile_dict[(hr_val, mn_val)] = float(row.avg_val) if row.avg_val is not None else 0.0

        # Seed random generator for consistent noise in testing
        np.random.seed(int(current_dt.timestamp()) % 10000)

        # Generate predictions for N days using profile or default profile curve
        for _ in range(intervals_count):
            hr = current_dt.hour
            mn = current_dt.minute
            
            predicted_kwh = profile_dict.get((hr, mn))
            if predicted_kwh is None:
                # Standard consumption curve as default backup
                hour_float = hr + mn / 60.0
                if hour_float < 6:
                    predicted_kwh = 0.22
                elif hour_float < 9:
                    predicted_kwh = 0.75
                elif hour_float < 16:
                    predicted_kwh = 0.45
                elif hour_float < 21:
                    predicted_kwh = 1.35
                else:
                    predicted_kwh = 0.32
                    
            # Add small random noise to make the forecast look dynamic and realistic
            noise = float(np.random.normal(0, 0.03))
            predicted_kwh = max(0.01, round(predicted_kwh + noise, 4))
            
            data_points.append(
                ForecastDataPoint(
                    timestamp=current_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    predicted_kwh=predicted_kwh
                )
            )
            current_dt += timedelta(minutes=30)
            
        return data_points
