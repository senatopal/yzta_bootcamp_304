from datetime import date, datetime
from typing import Any, Literal, Mapping

import requests

from dashboard.config.settings import API_TIMEOUT, BACKEND_URL

Period = Literal["half-hourly", "daily", "weekly", "monthly"]
DateValue = str | date | datetime
SimulationData = list[dict[str, Any]]
DeviceConfig = Mapping[str, Mapping[str, float]]


class APIClientError(RuntimeError):
    """Raised when a backend API request fails."""


class VoltiAPIClient:
    def __init__(
        self,
        base_url: str = BACKEND_URL,
        timeout: int = API_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    @staticmethod
    def _format_date(value: DateValue | None) -> str | None:
        if value is None:
            return None

        if isinstance(value, (date, datetime)):
            return value.isoformat()

        return value

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()

        except requests.Timeout as exc:
            raise APIClientError(
                "The backend request timed out."
            ) from exc

        except requests.ConnectionError as exc:
            raise APIClientError(
                "Could not connect to the backend. Please check whether the server is running."
            ) from exc

        except requests.HTTPError as exc:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text

            raise APIClientError(
                f"Backend error ({response.status_code}): {detail}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise APIClientError(
                "The backend returned an invalid JSON response."
            ) from exc

    def get_consumption_history(
        self,
        household_id: str,
        period: Period = "half-hourly",
        start_date: DateValue | None = None,
        end_date: DateValue | None = None,
    ) -> dict[str, Any]:
        params = {
            "household_id": household_id,
            "period": period,
            "start_date": self._format_date(start_date),
            "end_date": self._format_date(end_date),
        }

        # None olan parametreleri URL'ye gönderme.
        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return self._request(
            "GET",
            "/consumption/history",
            params=params,
        )

    def get_consumption_forecast(
        self,
        household_id: str,
        days: int = 1,
    ) -> dict[str, Any]:
        if not 1 <= days <= 7:
            raise ValueError("The days value must be between 1 and 7.")

        return self._request(
            "GET",
            "/consumption/forecast",
            params={
                "household_id": household_id,
                "days": days,
            },
        )

    @staticmethod
    def _create_simulation_payload(
        household_id: str,
        data: SimulationData,
        devices: DeviceConfig | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "household_id": household_id,
            "data": data,
        }

        if devices is not None:
            payload["devices"] = devices

        return payload

    def get_simulation_costs(
        self,
        household_id: str,
        data: SimulationData,
        devices: DeviceConfig | None = None,
    ) -> dict[str, Any]:
        payload = self._create_simulation_payload(
            household_id,
            data,
            devices,
        )

        return self._request(
            "POST",
            "/simulation/costs",
            json=payload,
        )

    def get_load_shift_recommendations(
        self,
        household_id: str,
        data: SimulationData,
        devices: DeviceConfig | None = None,
    ) -> dict[str, Any]:
        payload = self._create_simulation_payload(
            household_id,
            data,
            devices,
        )

        return self._request(
            "POST",
            "/simulation/recommendations/load-shift",
            json=payload,
        )

    def get_anomaly_alerts(
        self,
        household_id: str,
        data: SimulationData,
        devices: DeviceConfig | None = None,
    ) -> dict[str, Any]:
        payload = self._create_simulation_payload(
            household_id,
            data,
            devices,
        )

        return self._request(
            "POST",
            "/simulation/alerts/anomaly",
            json=payload,
        )

    def get_coach_context(
        self,
        household_id: str,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            "/coach/context",
            params={"household_id": household_id},
        )

    def close(self) -> None:
        self.session.close()


api_client = VoltiAPIClient()