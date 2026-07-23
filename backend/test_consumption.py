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
TEST_DB_FILE = "./test_consumption.db"
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
    
    # Insert half-hourly consumption readings
    readings = [
        # 2024-01-15 (Day 1, Week 3)
        ConsumptionReading(tstp=datetime(2024, 1, 15, 10, 0, 0), LCLid="MAC000002", energy_kwh=0.5, price_pence=10.0, cost_pounds=0.05),
        ConsumptionReading(tstp=datetime(2024, 1, 15, 10, 30, 0), LCLid="MAC000002", energy_kwh=1.0, price_pence=20.0, cost_pounds=0.20),
        # 2024-01-16 (Day 2, Week 3)
        ConsumptionReading(tstp=datetime(2024, 1, 16, 11, 0, 0), LCLid="MAC000002", energy_kwh=1.5, price_pence=15.0, cost_pounds=0.225),
        # 2024-02-15 (Month 2)
        ConsumptionReading(tstp=datetime(2024, 2, 15, 12, 0, 0), LCLid="MAC000002", energy_kwh=2.0, price_pence=12.0, cost_pounds=0.24)
    ]
    db.add_all(readings)
    db.commit()
    db.close()

def run_tests():
    print("=== Running Consumption History Endpoint Tests ===")
    setup_test_db()
    
    client = TestClient(app)
    
    # Test case 1: Retrieve raw half-hourly data
    print("[*] Test 1: GET half-hourly history")
    response = client.get("/api/v1/consumption/history?household_id=MAC000002&period=half-hourly")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res_data = response.json()
    assert res_data["household_id"] == "MAC000002"
    assert res_data["period"] == "half-hourly"
    assert len(res_data["data"]) == 4
    # Check values of first reading
    assert res_data["data"][0]["timestamp"] == "2024-01-15 10:00:00"
    assert res_data["data"][0]["consumption_kwh"] == 0.5
    assert res_data["data"][0]["cost_pounds"] == 0.05
    assert res_data["data"][0]["avg_price_pence"] == 10.0
    print("    -> PASS")

    # Test case 2: Retrieve aggregated daily data
    print("[*] Test 2: GET daily history")
    response = client.get("/api/v1/consumption/history?household_id=MAC000002&period=daily")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res_data = response.json()
    assert res_data["period"] == "daily"
    assert len(res_data["data"]) == 3 # 2024-01-15, 2024-01-16, 2024-02-15
    # Check aggregation values for 2024-01-15 (0.5 + 1.0 = 1.5 kwh, 0.05 + 0.20 = 0.25 pounds, avg price = (10 + 20) / 2 = 15 pence)
    day_1 = [d for d in res_data["data"] if d["timestamp"] == "2024-01-15"][0]
    assert day_1["consumption_kwh"] == 1.5
    assert day_1["cost_pounds"] == 0.25
    assert day_1["avg_price_pence"] == 15.0
    print("    -> PASS")

    # Test case 3: Retrieve aggregated weekly data
    print("[*] Test 3: GET weekly history")
    response = client.get("/api/v1/consumption/history?household_id=MAC000002&period=weekly")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res_data = response.json()
    assert res_data["period"] == "weekly"
    # Jan 15 and Jan 16 fall in the same week (week 2 or 3 depending on system, but they group together).
    # Since Feb 15 is in a different week, we expect 2 weeks in total.
    assert len(res_data["data"]) == 2
    print("    -> PASS")

    # Test case 4: Retrieve aggregated monthly data
    print("[*] Test 4: GET monthly history")
    response = client.get("/api/v1/consumption/history?household_id=MAC000002&period=monthly")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res_data = response.json()
    assert res_data["period"] == "monthly"
    assert len(res_data["data"]) == 2 # 2024-01 and 2024-02
    jan = [d for d in res_data["data"] if d["timestamp"] == "2024-01"][0]
    # Jan total = 0.5 + 1.0 + 1.5 = 3.0 kwh, total cost = 0.05 + 0.20 + 0.225 = 0.475 pounds
    assert jan["consumption_kwh"] == 3.0
    assert jan["cost_pounds"] == 0.475
    print("    -> PASS")

    # Test case 5: Invalid household
    print("[*] Test 5: GET history with non-existent household")
    response = client.get("/api/v1/consumption/history?household_id=UNKNOWN&period=daily")
    assert response.status_code == 200
    res_data = response.json()
    assert len(res_data["data"]) == 0
    print("    -> PASS")

    # Test case 6: Invalid period
    print("[*] Test 6: GET history with invalid period")
    response = client.get("/api/v1/consumption/history?household_id=MAC000002&period=invalid")
    assert response.status_code == 400
    print("    -> PASS")

    # Clean up test database file
    engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    print("=== All Tests Completed Successfully! ===")

if __name__ == "__main__":
    run_tests()
