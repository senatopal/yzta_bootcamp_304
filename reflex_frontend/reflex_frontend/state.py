import re
from typing import Any
from typing import Any, TypedDict
import httpx
import reflex as rx

class ChartPoint(TypedDict):
    timestamp: str
    value: float


class RecommendationCard(TypedDict):
    icon: str
    device: str
    time_shift: str
    saving: str
    carbon: str


class AnomalyCard(TypedDict):
    timestamp: str
    usage: str
    deviation: str

FASTAPI_URL = "http://127.0.0.1:8000/api/v1"

DEVICE_NAMES = {
    "Çamaşır Makinesi": "washing machine",
    "Bulaşık Makinesi": "dishwasher",
    "Kurutma Makinesi": "tumble dryer",
    "Kurutan Makine": "tumble dryer",
    "Elektrikli Araç Şarjı": "electric vehicle charger",
}


def extract_consumption_rows(
    payload: Any,
) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in (
            "data",
            "history",
            "records",
            "consumption",
        ):
            value = payload.get(key)

            if isinstance(value, list):
                return value

    return []


class DashboardState(rx.State):
    # Filters
    household_id: str = "MAC001074"
    start_date: str = "2012-11-01"
    end_date: str = "2012-11-07"

    # Page state
    is_loading: bool = False
    error_message: str = ""
    dashboard_loaded: bool = False

    # API responses
    consumption_data: dict[str, Any] = {}
    costs_data: dict[str, Any] = {}
    recommendations_data: dict[str, Any] = {}
    anomaly_data: dict[str, Any] = {}

    # Dashboard metrics
    total_consumption_kwh: float = 0.0
    total_cost_pounds: float = 0.0
    total_savings_pounds: float = 0.0
    carbon_kg: float = 0.0

    # Best recommendation
    best_action_title: str = ""
    best_action_message: str = ""

    forecast_days: int = 1

    history_chart_data: list[ChartPoint] = []
    forecast_chart_data: list[ChartPoint] = []

    recommendation_cards: list[RecommendationCard] = []
    anomaly_cards: list[AnomalyCard] = []

    anomaly_detected: bool = False
    anomaly_summary: str = ""

    total_anomaly_count: int = 0

    def reset_dashboard_result(self) -> None:
        self.dashboard_loaded = False
        self.error_message = ""

        self.consumption_data = {}
        self.costs_data = {}
        self.recommendations_data = {}
        self.anomaly_data = {}

        self.total_consumption_kwh = 0.0
        self.total_cost_pounds = 0.0
        self.total_savings_pounds = 0.0
        self.carbon_kg = 0.0

        self.best_action_title = ""
        self.best_action_message = ""

        self.history_chart_data = []
        self.forecast_chart_data = []

        self.recommendation_cards = []
        self.anomaly_cards = []

        self.anomaly_detected = False
        self.anomaly_summary = ""

        self.total_anomaly_count = 0

    @rx.event
    def update_household_id(self, value: str) -> None:
        self.household_id = value
        self.reset_dashboard_result()

    @rx.event
    def update_start_date(self, value: str) -> None:
        self.start_date = value
        self.reset_dashboard_result()

    @rx.event
    def update_end_date(self, value: str) -> None:
        self.end_date = value
        self.reset_dashboard_result()

    @rx.var
    def total_consumption_text(self) -> str:
        return f"{self.total_consumption_kwh:.2f} kWh"

    @rx.var
    def total_cost_text(self) -> str:
        return f"£{self.total_cost_pounds:.2f}"

    @rx.var
    def total_savings_text(self) -> str:
        return f"£{self.total_savings_pounds:.2f}"

    @rx.var
    def carbon_text(self) -> str:
        return f"{self.carbon_kg:.2f} kg"

    @rx.var
    def recommendation_count_text(self) -> str:
        recommendations = self.recommendations_data.get(
            "recommendations",
            [],
        )

        count = len(recommendations)

        if count == 1:
            return "1 personalised recommendation"

        return f"{count} personalised recommendations"
    
    @rx.var
    def anomaly_count_text(self) -> str:
        count = self.total_anomaly_count

        if count == 1:
            return "1 potential anomaly detected"

        return f"{count} potential anomalies detected"


    @rx.event
    async def load_dashboard(self):
        self.reset_dashboard_result()

        household_id = self.household_id.strip().upper()

        if not re.fullmatch(r"MAC\d{6}", household_id):
            self.error_message = (
                "Household ID must follow the format MAC000000."
            )
            return

        if not self.start_date or not self.end_date:
            self.error_message = "Please select both dates."
            return

        if self.start_date > self.end_date:
            self.error_message = (
                "Start date cannot be later than end date."
            )
            return

        self.household_id = household_id
        self.is_loading = True
        yield

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                # 1. Consumption history
                history_response = await client.get(
                    f"{FASTAPI_URL}/consumption/history",
                    params={
                        "household_id": household_id,
                        "period": "half-hourly",
                        "start_date": (
                            f"{self.start_date}T00:00:00"
                        ),
                        "end_date": (
                            f"{self.end_date}T23:59:59"
                        ),
                    },
                )

                history_response.raise_for_status()
                history_payload = history_response.json()

                records = extract_consumption_rows(
                    history_payload
                )

                if not records:
                    self.error_message = (
                        "No consumption data was found for "
                        f"{household_id} in the selected date range."
                    )
                    return

                self.consumption_data = history_payload

                self.history_chart_data = [
                    {
                        "timestamp": str(
                            item.get("timestamp", "")
                        )[5:16],
                        "value": round(
                            float(item.get("consumption_kwh") or 0.0),
                            3,
                        ),
                    }
                    for item in records
                ]

                # 2. Consumption forecast
                forecast_response = await client.get(
                    f"{FASTAPI_URL}/consumption/forecast",
                    params={
                        "household_id": household_id,
                        "days": self.forecast_days,
                    },
                )

                forecast_response.raise_for_status()
                forecast_payload = forecast_response.json()

                forecast_rows = forecast_payload.get("data", [])

                self.forecast_chart_data = [
                    {
                        "timestamp": str(
                            item.get("timestamp", "")
                        )[5:16],
                        "value": round(
                            float(item.get("predicted_kwh") or 0.0),
                            3,
                        ),
                    }
                    for item in forecast_rows
                ]

                # Convert history response to SimulationRequest format
                simulation_rows = [
                    {
                        "tstp": str(
                            item.get("timestamp", "")
                        ).replace(" ", "T"),
                        "energy(kWh/hh)": float(
                            item.get("consumption_kwh") or 0.0
                        ),
                        "price_pence": float(
                            item.get("avg_price_pence") or 0.0
                        ),
                    }
                    for item in records
                ]

                simulation_payload = {
                    "household_id": household_id,
                    "data": simulation_rows,
                    "devices": {},
                }

                # 2. Costs and carbon
                costs_response = await client.post(
                    f"{FASTAPI_URL}/simulation/costs",
                    json=simulation_payload,
                )
                costs_response.raise_for_status()

                costs_payload = costs_response.json()
                self.costs_data = costs_payload

                self.total_consumption_kwh = float(
                    costs_payload.get(
                        "total_consumption_kwh",
                        0.0,
                    )
                    or 0.0
                )

                self.total_cost_pounds = float(
                    costs_payload.get(
                        "total_cost_pounds",
                        0.0,
                    )
                    or 0.0
                )

                carbon_impact = costs_payload.get(
                    "carbon_impact",
                    {},
                )

                self.carbon_kg = float(
                    carbon_impact.get("carbon_kg", 0.0)
                    or 0.0
                )

                # 3. Load-shifting recommendations
                recommendations_response = await client.post(
                    f"{FASTAPI_URL}/recommendations/load-shift",
                    json=simulation_payload,
                )
                recommendations_response.raise_for_status()

                recommendations_payload = (
                    recommendations_response.json()
                )

                self.recommendations_data = (
                    recommendations_payload
                )

                self.total_savings_pounds = float(
                    recommendations_payload.get(
                        "total_savings_pounds",
                        0.0,
                    )
                    or 0.0
                )

                recommendations = (
                    recommendations_payload.get(
                        "recommendations",
                        [],
                    )
                )

                self.recommendation_cards = [
                    {
                        "icon": str(item.get("icon", "⚡")),
                        "device": DEVICE_NAMES.get(
                            str(item.get("device", "")),
                            str(item.get("device", "Appliance")),
                        ).title(),
                        "time_shift": (
                            f"{item.get('current_hour', '—')} → "
                            f"{item.get('recommended_hour', '—')}"
                        ),
                        "saving": (
                            f"£{float(item.get('estimated_savings_pounds') or 0):.2f}"
                        ),
                        "carbon": (
                            f"{float(item.get('carbon_reduction_kg') or 0):.2f} kg CO₂"
                        ),
                    }
                    for item in recommendations
                ]

                if recommendations:
                    top_recommendation = max(
                        recommendations,
                        key=lambda item: float(
                            item.get(
                                "estimated_savings_pounds",
                                0.0,
                            )
                            or 0.0
                        ),
                    )

                    raw_device = top_recommendation.get(
                        "device",
                        "appliance",
                    )

                    device = DEVICE_NAMES.get(
                        raw_device,
                        raw_device,
                    )

                    current_hour = top_recommendation.get(
                        "current_hour",
                        "the current time",
                    )

                    recommended_hour = (
                        top_recommendation.get(
                            "recommended_hour",
                            "a cheaper period",
                        )
                    )

                    saving = float(
                        top_recommendation.get(
                            "estimated_savings_pounds",
                            0.0,
                        )
                        or 0.0
                    )

                    self.best_action_title = (
                        f"Run your {device} at "
                        f"{recommended_hour}"
                    )

                    self.best_action_message = (
                        f"Move it from {current_hour} to "
                        f"{recommended_hour} to save approximately "
                        f"£{saving:.2f}."
                    )

                else:
                    self.best_action_title = (
                        "No load-shifting savings found"
                    )

                    self.best_action_message = (
                        "The selected period does not currently "
                        "contain a useful lower-cost appliance shift."
                    )

                # 4. Anomalies
                anomaly_response = await client.post(
                    f"{FASTAPI_URL}/alerts/anomaly",
                    json=simulation_payload,
                )
                anomaly_response.raise_for_status()

                self.anomaly_data = anomaly_response.json()

                self.anomaly_detected = bool(
                    self.anomaly_data.get("anomaly_detected", False)
                )

                self.anomaly_summary = (
                    "We detected unusual energy use. A device may have been left running."
                    if self.anomaly_detected
                    else "No unusual energy use was detected."
                )

                anomalies = self.anomaly_data.get("anomalies", [])

                self.total_anomaly_count = len(anomalies)

                self.anomaly_cards = [
                    {
                        "timestamp": str(
                            item.get("timestamp", "Unknown time")
                        ),
                        "usage": (
                            f"Expected {float(item.get('expected_kwh') or 0):.2f} kWh "
                            f"· Actual {float(item.get('actual_kwh') or 0):.2f} kWh"
                        ),
                        "deviation": (
                            f"{float(item.get('deviation_percent') or 0):.1f}% above expected"
                        ),
                    }
                    for item in anomalies[:20]
                ]

                self.dashboard_loaded = True

        except httpx.HTTPStatusError as exc:
            self.error_message = (
                "Backend returned error "
                f"{exc.response.status_code}: "
                f"{exc.response.text[:200]}"
            )

        except httpx.RequestError:
            self.error_message = (
                "Could not connect to the FastAPI backend "
                "on port 8000."
            )

        except (TypeError, ValueError, KeyError) as exc:
            self.error_message = (
                f"The backend response could not be processed: {exc}"
            )

        finally:
            self.is_loading = False