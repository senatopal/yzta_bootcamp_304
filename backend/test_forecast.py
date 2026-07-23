import os
import sys
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Put current backend dir in path for local imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from app.core.database import Base, get_db
from app.models.household import Household
from app.models.consumption import ConsumptionReading

# Define a test SQLite database file
TEST_DB_FILE = "./test_forecast.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def setup_test_db():
    # Recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Insert a test household
    hh = Household(LCLid="MAC000002", stdorToU="ToU", acorn_grouped="Affluent")
    db.add(hh)
    
    # Insert some historical consumption readings
    # To test average hourly profiling, let's add reading at 10:00 and 10:30
    readings = [
        ConsumptionReading(tstp=datetime(2024, 1, 15, 10, 0, 0), LCLid="MAC000002", energy_kwh=0.8, price_pence=15.0, cost_pounds=0.12),
        ConsumptionReading(tstp=datetime(2024, 1, 15, 10, 30, 0), LCLid="MAC000002", energy_kwh=1.2, price_pence=18.0, cost_pounds=0.216),
        ConsumptionReading(tstp=datetime(2024, 1, 16, 10, 0, 0), LCLid="MAC000002", energy_kwh=0.6, price_pence=15.0, cost_pounds=0.09)
    ]
    db.add_all(readings)
    db.commit()
    db.close()

def run_tests():
    print("=== Running Consumption Forecast Endpoint Tests ===")
    setup_test_db()
    
    client = TestClient(app)
    
    # Test case 1: Retrieve 1-day forecast (48 slots)
    print("[*] Test 1: GET 1-day forecast (defaults to latest datetime)")
    response = client.get("/api/v1/consumption/forecast?household_id=MAC000002&days=1")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res_data = response.json()
    assert res_data["household_id"] == "MAC000002"
    assert res_data["forecast_days"] == 1
    assert len(res_data["data"]) == 48
    # Should start from latest reading + 30 minutes (2024-01-16 10:00:00 + 30m = 10:30:00)
    assert res_data["data"][0]["timestamp"] == "2024-01-16 10:30:00"
    print("    -> PASS")

    # Test case 2: Retrieve forecast with custom start date
    print("[*] Test 2: GET forecast with custom start_date")
    custom_start = "2024-02-01T12:00:00"
    response = client.get(f"/api/v1/consumption/forecast?household_id=MAC000002&days=1&start_date={custom_start}")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["data"][0]["timestamp"] == "2024-02-01 12:00:00"
    print("    -> PASS")

    # Test case 3: Retrieve 3-day forecast (144 slots)
    print("[*] Test 3: GET 3-day forecast")
    response = client.get("/api/v1/consumption/forecast?household_id=MAC000002&days=3")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["forecast_days"] == 3
    assert len(res_data["data"]) == 144
    print("    -> PASS")

    # Test case 4: Forecast fallback for unknown household (uses default profiles)
    print("[*] Test 4: GET forecast for non-existent household (fallback to global or default)")
    response = client.get("/api/v1/consumption/forecast?household_id=UNKNOWN&days=1")
    assert response.status_code == 200
    res_data = response.json()
    assert len(res_data["data"]) == 48
    # Verify predictions are populated
    assert all(item["predicted_kwh"] > 0 for item in res_data["data"])
    print("    -> PASS")

    # Test case 5: Validation for days > 7 (should fail)
    print("[*] Test 5: GET forecast with too many days (> 7)")
    response = client.get("/api/v1/consumption/forecast?household_id=MAC000002&days=8")
    assert response.status_code == 422 # Pydantic validation error
    print("    -> PASS")

    # Clean up database resources
    engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    print("=== All Tests Completed Successfully! ===")

if __name__ == "__main__":
    run_tests()
