import os
import sys
from datetime import datetime, timedelta
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

TEST_DB_FILE = "./test_coach.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    
    # 1. Insert a test household
    hh = Household(LCLid="MAC000002", stdorToU="ToU", acorn_grouped="Affluent")
    db.add(hh)
    
    # 2. Insert 7 days of consumption readings
    # Seed hourly/half-hourly data.
    # Normal days: 0.2 kwh, 15 pence price
    # We will simulate 7 days: July 15 to July 22, 2026.
    base_time = datetime(2026, 7, 22, 12, 0, 0)
    readings = []
    
    for hours_ago in range(0, 7 * 24 * 2): # half-hourly slots
        tstp = base_time - timedelta(minutes=30 * hours_ago)
        
        # Default consumption
        energy = 0.2
        price = 15.0
        
        # Peak prices at 18:00 - 20:00 (say 28.0 pence)
        # Off-peak prices at 01:00 - 04:00 (say 10.0 pence)
        if 18 <= tstp.hour <= 20:
            price = 28.0
        elif 1 <= tstp.hour <= 4:
            price = 10.0
            
        # Simulate one anomaly consumption spike on July 20 at 19:30
        if tstp.year == 2026 and tstp.month == 7 and tstp.day == 20 and tstp.hour == 19 and tstp.minute == 30:
            energy = 3.0 # Anomaly! 15x normal load
            
        cost = (energy * price) / 100
        
        readings.append(
            ConsumptionReading(
                tstp=tstp,
                LCLid="MAC000002",
                energy_kwh=energy,
                price_pence=price,
                cost_pounds=cost
            )
        )
        
    db.add_all(readings)
    db.commit()
    db.close()

def run_tests():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print("=== Running LLM Coach Context Endpoint Tests ===")
    setup_test_db()
    
    client = TestClient(app)
    
    # Test case 1: Query existing household
    print("[*] Test 1: GET /api/v1/coach/context for existing household")
    response = client.get("/api/v1/coach/context?household_id=MAC000002")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    res_data = response.json()
    assert res_data["household_id"] == "MAC000002"
    assert res_data["weekly_summary"] is not None
    assert res_data["weekly_summary"]["total_consumption_kwh"] > 0
    assert res_data["weekly_summary"]["total_cost_pounds"] > 0
    assert len(res_data["cheapest_hours"]) == 3
    assert len(res_data["expensive_hours"]) == 3
    assert len(res_data["recommendations"]) > 0
    assert len(res_data["anomalies"]) > 0 # Anomaly must be detected
    
    prompt = res_data["prompt_context"]
    print("\n--- Prompt Context Output ---")
    print(prompt)
    print("-----------------------------\n")
    
    # Confirm prompt strings contain vital grounding data
    assert "Volti Energy Coach" in prompt
    assert "MAC000002" in prompt
    assert "WARNING: Potential energy waste / abnormal usage" in prompt
    assert "Load Shifting Recommendations" in prompt
    print("    -> PASS")

    # Test case 2: Query non-existent household (should return 404)
    print("[*] Test 2: GET /api/v1/coach/context for non-existent household")
    response = client.get("/api/v1/coach/context?household_id=UNKNOWN")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print("    -> PASS")

    # Clean up test database file
    engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    print("=== All Coach Tests Completed Successfully! ===")

if __name__ == "__main__":
    run_tests()
