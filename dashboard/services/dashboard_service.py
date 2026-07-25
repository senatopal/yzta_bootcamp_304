from typing import Any

from dashboard.api.client import (
    APIClientError,
    DeviceConfig,
    Period,
    VoltiAPIClient,
    api_client,
)


class DashboardService:
    """Collects and prepares API data required by the dashboard."""

    def __init__(self, client: VoltiAPIClient = api_client) -> None:
        self.client = client

    @staticmethod
    def _build_simulation_data(
        consumption_history: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Converts consumption history response into the request format
        expected by simulation endpoints.
        """
        simulation_data = []

        for item in consumption_history.get("data", []):
            simulation_data.append(
                {
                    "tstp": item["timestamp"],
                    "energy(kWh/hh)": item.get(
                        "consumption_kwh",
                        0.0,
                    ),
                    "price_pence": item.get(
                        "avg_price_pence",
                        0.0,
                    ),
                }
            )

        return simulation_data

    def get_dashboard_data(
        self,
        household_id: str,
        period: Period = "half-hourly",
        forecast_days: int = 1,
        start_date: str | None = None,
        end_date: str | None = None,
        devices: DeviceConfig | None = None,
    ) -> dict[str, Any]:
        """
        Fetches all data required by the Volti dashboard.
        """
        consumption = self.client.get_consumption_history(
            household_id=household_id,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )

        simulation_data = self._build_simulation_data(consumption)

        forecast = self.client.get_consumption_forecast(
            household_id=household_id,
            days=forecast_days,
        )

        costs = self.client.get_simulation_costs(
            household_id=household_id,
            data=simulation_data,
            devices=devices,
        )

        recommendations = (
            self.client.get_load_shift_recommendations(
                household_id=household_id,
                data=simulation_data,
                devices=devices,
            )
        )

        anomaly = self.client.get_anomaly_alerts(
            household_id=household_id,
            data=simulation_data,
            devices=devices,
        )

        coach_context = self.client.get_coach_context(
            household_id=household_id,
        )

        return {
            "household_id": household_id,
            "consumption": consumption,
            "forecast": forecast,
            "costs": costs,
            "recommendations": recommendations,
            "anomaly": anomaly,
            "coach_context": coach_context,
        }


dashboard_service = DashboardService()