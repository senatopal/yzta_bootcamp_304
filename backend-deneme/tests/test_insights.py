import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.simulation import SimulationService


def test_load_shift_recommendations_returns_savings_and_carbon_values():
    df = pd.DataFrame(
        [
            {"tstp": "2026-07-22T18:00:00", "energy(kWh/hh)": 1.2, "price_pence": 28.0},
            {"tstp": "2026-07-22T02:00:00", "energy(kWh/hh)": 0.5, "price_pence": 12.0},
            {"tstp": "2026-07-22T19:00:00", "energy(kWh/hh)": 0.8, "price_pence": 24.0},
        ]
    )

    result = SimulationService.generate_load_shift_recommendations(df, household_id="MAC0001")

    assert result["household_id"] == "MAC0001"
    assert result["recommended_hour"] == "02:00"
    assert len(result["recommendations"]) >= 2
    assert result["recommendations"][0]["estimated_savings_pounds"] >= 0
    assert result["recommendations"][0]["carbon_reduction_kg"] >= 0


def test_anomaly_detection_flags_high_usage():
    df = pd.DataFrame(
        [
            {"tstp": "2026-07-22T18:00:00", "energy(kWh/hh)": 0.4, "price_pence": 20.0},
            {"tstp": "2026-07-22T18:30:00", "energy(kWh/hh)": 0.45, "price_pence": 21.0},
            {"tstp": "2026-07-22T19:00:00", "energy(kWh/hh)": 0.42, "price_pence": 22.0},
            {"tstp": "2026-07-22T19:30:00", "energy(kWh/hh)": 2.4, "price_pence": 23.0},
        ]
    )

    result = SimulationService.detect_anomaly(df, household_id="MAC0002")

    assert result["household_id"] == "MAC0002"
    assert result["anomaly_detected"] is True
    assert result["sapma_yuzde"] >= 0


def test_carbon_calculation_returns_value_in_kg():
    result = SimulationService.calculate_carbon_impact(2.5, emission_factor_kg_per_kwh=0.21)

    assert result["energy_kwh"] == 2.5
    assert result["carbon_kg"] == 0.525
