from __future__ import annotations
from collections import defaultdict
from typing import Any, TypedDict

import re
import os
import httpx
import reflex as rx


FASTAPI_ROOT = os.getenv(
    "FASTAPI_ROOT",
    "http://127.0.0.1:8000",
).rstrip("/")

FASTAPI_URL = f"{FASTAPI_ROOT}/api/v1"

DEVICE_NAMES = {
    "Çamaşır Makinesi": "washing machine",
    "Bulaşık Makinesi": "dishwasher",
    "Kurutma Makinesi": "tumble dryer",
    "Kurutan Makine": "tumble dryer",
    "Elektrikli Araç Şarjı": "electric vehicle charger",
}


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


class HourlyPoint(TypedDict):
    hour: str
    consumption: float
    cost: float


class CoachChatMessage(TypedDict):
    role: str
    content: str


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value if value is not None else default)
    except (TypeError, ValueError):
        return default


def extract_list(
    payload: Any,
    keys: tuple[str, ...],
) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def extract_consumption_rows(payload: Any) -> list[dict[str, Any]]:
    return extract_list(
        payload,
        ("data", "history", "records", "consumption"),
    )


def create_hourly_fallback(
    records: list[dict[str, Any]],
) -> list[HourlyPoint]:
    totals: dict[str, dict[str, float]] = defaultdict(
        lambda: {"consumption": 0.0, "cost": 0.0}
    )

    for item in records:
        timestamp = str(item.get("timestamp", ""))
        hour = timestamp[11:13]

        if not hour:
            continue

        label = f"{hour}:00"
        totals[label]["consumption"] += to_float(
            item.get("consumption_kwh")
        )
        totals[label]["cost"] += to_float(item.get("cost_pounds"))

    return [
        {
            "hour": hour,
            "consumption": round(values["consumption"], 3),
            "cost": round(values["cost"], 2),
        }
        for hour, values in sorted(totals.items())
    ]


def parse_hour_rows(payload: Any) -> list[HourlyPoint]:
    rows = extract_list(
        payload,
        ("data", "hours", "hourly_data", "hourly_breakdown"),
    )
    parsed: list[HourlyPoint] = []

    for item in rows:
        raw_hour = (
            item.get("hour")
            or item.get("time_slot")
            or item.get("timestamp")
            or ""
        )
        hour = str(raw_hour)

        if len(hour) >= 16:
            hour = hour[11:16]

        if not hour:
            continue

        parsed.append(
            {
                "hour": hour,
                "consumption": round(
                    to_float(
                        item.get("consumption_kwh")
                        or item.get("energy_kwh")
                        or item.get("total_consumption_kwh")
                    ),
                    3,
                ),
                "cost": round(
                    to_float(
                        item.get("cost_pounds")
                        or item.get("total_cost_pounds")
                    ),
                    2,
                ),
            }
        )

    return parsed


def translate_device(device: Any) -> str:
    raw_device = str(device or "appliance")
    return DEVICE_NAMES.get(raw_device, raw_device)


def create_coach_message(
    coach_payload: dict[str, Any],
    *,
    selected_consumption_kwh: float,
    selected_cost_pounds: float,
    fallback_recommendation: str,
    anomaly_detected: bool,
) -> str:
    parts: list[str] = []

    weekly_summary = coach_payload.get("weekly_summary")
    if isinstance(weekly_summary, dict):
        weekly_consumption = to_float(
            weekly_summary.get("total_consumption_kwh")
        )
        weekly_cost = to_float(weekly_summary.get("total_cost_pounds"))

        parts.append(
            "I have loaded the latest available household data. "
            f"During the latest week, your home used "
            f"{weekly_consumption:.2f} kWh and cost approximately "
            f"£{weekly_cost:.2f}."
        )
    else:
        parts.append(
            "I have loaded the selected household data. "
            f"The selected period used {selected_consumption_kwh:.2f} kWh "
            f"and cost approximately £{selected_cost_pounds:.2f}."
        )

    recommendations = coach_payload.get("recommendations")
    if isinstance(recommendations, list) and recommendations:
        recommendation = recommendations[0]
        if isinstance(recommendation, dict):
            device = translate_device(recommendation.get("device"))
            recommended_hour = recommendation.get(
                "recommended_hour", "a cheaper period"
            )
            saving = to_float(
                recommendation.get("estimated_savings_pounds")
            )
            parts.append(
                f"One useful option is to run your {device} at "
                f"{recommended_hour}, with an estimated saving of "
                f"£{saving:.2f}."
            )
    elif fallback_recommendation:
        parts.append(fallback_recommendation)

    coach_anomalies = coach_payload.get("anomalies")
    has_coach_anomaly = (
        isinstance(coach_anomalies, list) and bool(coach_anomalies)
    )

    if has_coach_anomaly or anomaly_detected:
        parts.append(
            "Unusual consumption was detected, so it may be worth checking "
            "whether an appliance was left running."
        )
    else:
        parts.append("No unusual consumption was detected.")

    parts.append("Ask me a question about this household's energy use.")
    return " ".join(parts)


class DashboardState(rx.State):
    household_id: str = "MAC001074"
    start_date: str = "2012-11-01"
    end_date: str = "2012-11-07"
    forecast_days: int = 1

    best_action_title: str = ""
    best_action_message: str = ""
    best_action_device: str = ""

    is_loading: bool = False
    error_message: str = ""
    partial_data_message: str = ""
    dashboard_loaded: bool = False

    backend_online: bool = False
    backend_status: str = "Checking services..."
    households_loaded: bool = False

    household_ids: list[str] = []
    available_household_count: int = 0
    household_tariff: str = ""
    household_group: str = ""

    consumption_data: dict[str, Any] = {}
    costs_data: dict[str, Any] = {}
    recommendations_data: dict[str, Any] = {}
    anomaly_data: dict[str, Any] = {}
    hours_data: dict[str, Any] = {}
    coach_context_data: dict[str, Any] = {}

    total_consumption_kwh: float = 0.0
    total_cost_pounds: float = 0.0
    total_savings_pounds: float = 0.0
    carbon_kg: float = 0.0

    history_chart_data: list[ChartPoint] = []
    forecast_chart_data: list[ChartPoint] = []
    hourly_chart_data: list[HourlyPoint] = []
    recommendation_cards: list[RecommendationCard] = []
    anomaly_cards: list[AnomalyCard] = []

    best_action_title: str = ""
    best_action_message: str = ""

    anomaly_detected: bool = False
    anomaly_summary: str = ""
    total_anomaly_count: int = 0

    coach_message: str = ""
    coach_prompt_context: str = ""
    coach_context_available: bool = False
    coach_open: bool = False
    coach_input: str = ""
    coach_messages: list[CoachChatMessage] = []
    coach_is_sending: bool = False
    coach_error: str = ""
    coach_model: str = ""

    # First-use chart walkthrough.
    tour_open: bool = False
    tour_step: int = 0
    tour_seen: str = rx.LocalStorage(
        name="volti_chart_tour_seen",
    )

    def reset_dashboard_result(self) -> None:
        self.dashboard_loaded = False
        self.error_message = ""
        self.partial_data_message = ""

        self.household_tariff = ""
        self.household_group = ""

        self.consumption_data = {}
        self.costs_data = {}
        self.recommendations_data = {}
        self.anomaly_data = {}
        self.hours_data = {}
        self.coach_context_data = {}

        self.total_consumption_kwh = 0.0
        self.total_cost_pounds = 0.0
        self.total_savings_pounds = 0.0
        self.carbon_kg = 0.0

        self.history_chart_data = []
        self.forecast_chart_data = []
        self.hourly_chart_data = []
        self.recommendation_cards = []
        self.anomaly_cards = []

        self.recommendation_cards = []
        self.best_action_device = ""
        self.best_action_title = ""
        self.best_action_message = ""

        self.anomaly_detected = False
        self.anomaly_summary = ""
        self.total_anomaly_count = 0

        self.coach_message = ""
        self.coach_prompt_context = ""
        self.coach_context_available = False
        self.coach_input = ""
        self.coach_messages = []
        self.coach_is_sending = False
        self.coach_error = ""
        self.coach_model = ""

        self.tour_open = False
        self.tour_step = 0

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

    @rx.event
    def update_coach_input(self, value: str) -> None:
        self.coach_input = value

    @rx.event
    def toggle_coach(self) -> None:
        self.coach_open = not self.coach_open
        self.coach_error = ""

    @rx.event
    def clear_coach_chat(self) -> None:
        self.coach_error = ""
        self.coach_input = ""
        self.coach_model = ""

        if self.coach_message:
            self.coach_messages = [
                {
                    "role": "assistant",
                    "content": self.coach_message,
                }
            ]
        else:
            self.coach_messages = []

    @rx.event
    def start_chart_tour(self) -> None:
        if not self.dashboard_loaded:
            return
        self.tour_step = 0
        self.tour_open = True

    @rx.event
    def next_chart_tour_step(self) -> None:
        if self.tour_step < 2:
            self.tour_step += 1
        else:
            self.tour_open = False
            self.tour_seen = "true"

    @rx.event
    def previous_chart_tour_step(self) -> None:
        if self.tour_step > 0:
            self.tour_step -= 1

    @rx.event
    def close_chart_tour(self) -> None:
        self.tour_open = False
        self.tour_seen = "true"

    @rx.var
    def tour_step_label(self) -> str:
        return f"STEP {self.tour_step + 1} OF 3"

    @rx.var
    def tour_title(self) -> str:
        titles = (
            "Consumption history",
            "Next 24-hour forecast",
            "Hourly energy breakdown",
        )
        return titles[min(max(self.tour_step, 0), 2)]

    @rx.var
    def tour_description(self) -> str:
        descriptions = (
            (
                "The horizontal axis shows time and the vertical axis shows "
                "electricity use in kWh. Sharp peaks mark periods when the "
                "household used more electricity."
            ),
            (
                "The orange line shows predicted electricity use for the "
                "coming 24 hours. Higher points indicate periods when demand "
                "is expected to increase."
            ),
            (
                "Each bar groups total electricity use by hour of the day. "
                "Taller bars reveal the hours with the highest consumption."
            ),
        )
        return descriptions[min(max(self.tour_step, 0), 2)]

    @rx.var
    def tour_tip(self) -> str:
        tips = (
            "Look for repeated peaks to identify high-use routines.",
            "Use the forecast to plan flexible appliances before demand rises.",
            "Compare bar heights to find the best hours to shift usage away from.",
        )
        return tips[min(max(self.tour_step, 0), 2)]

    @rx.var
    def tour_next_label(self) -> str:
        return "Finish" if self.tour_step == 2 else "Next"

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
        count = len(self.recommendation_cards)
        if count == 1:
            return "1 personalised recommendation"
        return f"{count} personalised recommendations"

    @rx.var
    def anomaly_count_text(self) -> str:
        if self.total_anomaly_count == 1:
            return "1 potential anomaly detected"
        return f"{self.total_anomaly_count} potential anomalies detected"

    @rx.var
    def household_count_text(self) -> str:
        if not self.households_loaded:
            return "Household list unavailable"
        return f"{self.available_household_count} households available"

    @rx.var
    def household_profile_text(self) -> str:
        tariff = self.household_tariff or "Unknown tariff"
        group = self.household_group or "Unknown group"
        return f"{tariff} tariff · {group}"

    @rx.event
    async def initialize_page(self):
        self.backend_status = "Checking services..."
        self.households_loaded = False

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                health_response = await client.get(f"{FASTAPI_ROOT}/health")
                health_response.raise_for_status()
                self.backend_online = True
                self.backend_status = "Services online"
            except httpx.HTTPError:
                self.backend_online = False
                self.backend_status = "Backend unavailable"
                self.household_ids = []
                self.available_household_count = 0
                return

            try:
                households_response = await client.get(
                    f"{FASTAPI_URL}/households"
                )
                households_response.raise_for_status()
                payload = households_response.json()
                households = extract_list(
                    payload,
                    ("data", "households", "items"),
                )

                ids: list[str] = []
                for item in households:
                    item_id = (
                        item.get("LCLid")
                        or item.get("lclid")
                        or item.get("household_id")
                    )
                    if item_id:
                        ids.append(str(item_id).upper())

                self.household_ids = sorted(set(ids))
                self.available_household_count = len(self.household_ids)
                self.households_loaded = True
            except (httpx.HTTPError, TypeError, ValueError):
                self.household_ids = []
                self.available_household_count = 0
                self.households_loaded = False

    @rx.event
    async def send_coach_message(self):
        message = self.coach_input.strip()

        if not message or self.coach_is_sending:
            return

        household_id = self.household_id.strip().upper()

        if not re.fullmatch(r"MAC\d{6}", household_id):
            self.coach_error = (
                "Load a valid household before asking the energy coach."
            )
            return

        if not self.dashboard_loaded:
            self.coach_error = (
                "Load the dashboard before asking a household-specific question."
            )
            return

        history = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in self.coach_messages[-10:]
            if item["role"] in {"user", "assistant"}
            and item["content"].strip()
        ]

        self.coach_messages = [
            *self.coach_messages,
            {"role": "user", "content": message},
        ]
        self.coach_input = ""
        self.coach_error = ""
        self.coach_is_sending = True
        yield

        try:
            async with httpx.AsyncClient(timeout=75.0) as client:
                response = await client.post(
                    f"{FASTAPI_URL}/coach/chat",
                    json={
                        "household_id": household_id,
                        "message": message,
                        "history": history,
                    },
                )
                response.raise_for_status()
                payload = response.json()

            answer = str(payload.get("answer") or "").strip()
            if not answer:
                raise ValueError("The coach returned an empty answer.")

            self.coach_messages = [
                *self.coach_messages,
                {"role": "assistant", "content": answer},
            ]
            self.coach_model = str(payload.get("model") or "Gemini")
            self.coach_context_available = bool(
                payload.get("grounded", True)
            )

        except httpx.HTTPStatusError as exc:
            try:
                detail = str(exc.response.json().get("detail") or "")
            except (ValueError, AttributeError):
                detail = ""

            if exc.response.status_code == 429:
                self.coach_error = (
                    "The AI coach is receiving too many requests. "
                    "Please try again shortly."
                )
            elif exc.response.status_code in {502, 503}:
                self.coach_error = (
                    detail
                    or "The Gemini coach is temporarily unavailable."
                )
            else:
                self.coach_error = (
                    detail
                    or f"Coach request failed with status "
                    f"{exc.response.status_code}."
                )

        except httpx.RequestError:
            self.coach_error = (
                "Could not connect to the Coach API on port 8000."
            )
        except (TypeError, ValueError, KeyError) as exc:
            self.coach_error = (
                f"The coach response could not be processed: {exc}"
            )
        finally:
            self.coach_is_sending = False

    @rx.event
    async def load_dashboard(self):
        self.reset_dashboard_result()

        household_id = self.household_id.strip().upper()

        if not re.fullmatch(r"MAC\d{6}", household_id):
            self.error_message = (
                "Household ID must follow the format MAC000000."
            )
            return

        if self.household_ids and household_id not in self.household_ids:
            self.error_message = f"Household {household_id} does not exist."
            return

        if not self.start_date or not self.end_date:
            self.error_message = "Please select both dates."
            return

        if self.start_date > self.end_date:
            self.error_message = "Start date cannot be later than end date."
            return

        self.household_id = household_id
        self.is_loading = True
        yield

        optional_failures: list[str] = []

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                try:
                    profile_response = await client.get(
                        f"{FASTAPI_URL}/households/{household_id}"
                    )
                    profile_response.raise_for_status()
                    profile_payload = profile_response.json()
                    self.household_tariff = str(
                        profile_payload.get("stdorToU") or "Unknown"
                    )
                    self.household_group = str(
                        profile_payload.get("acorn_grouped") or "Unknown"
                    )
                except (httpx.HTTPError, TypeError, ValueError):
                    self.household_tariff = "Unknown"
                    self.household_group = "Unknown"
                    optional_failures.append("household profile")

                history_response = await client.get(
                    f"{FASTAPI_URL}/consumption/history",
                    params={
                        "household_id": household_id,
                        "period": "half-hourly",
                        "start_date": f"{self.start_date}T00:00:00",
                        "end_date": f"{self.end_date}T23:59:59",
                    },
                )
                history_response.raise_for_status()
                history_payload = history_response.json()
                records = extract_consumption_rows(history_payload)

                if not records:
                    self.error_message = (
                        "No consumption data was found for "
                        f"{household_id} in the selected date range."
                    )
                    return

                self.consumption_data = history_payload
                self.history_chart_data = [
                    {
                        "timestamp": str(item.get("timestamp", ""))[5:16],
                        "value": round(
                            to_float(item.get("consumption_kwh")),
                            3,
                        ),
                    }
                    for item in records
                ]

                try:
                    forecast_response = await client.get(
                        f"{FASTAPI_URL}/consumption/forecast",
                        params={
                            "household_id": household_id,
                            "days": self.forecast_days,
                        },
                    )
                    forecast_response.raise_for_status()
                    forecast_payload = forecast_response.json()
                    forecast_rows = extract_list(
                        forecast_payload,
                        ("data", "forecast", "predictions"),
                    )
                    self.forecast_chart_data = [
                        {
                            "timestamp": str(
                                item.get("timestamp", "")
                            )[5:16],
                            "value": round(
                                to_float(item.get("predicted_kwh")),
                                3,
                            ),
                        }
                        for item in forecast_rows
                    ]
                except (httpx.HTTPError, TypeError, ValueError):
                    self.forecast_chart_data = []
                    optional_failures.append("forecast")

                simulation_rows = [
                    {
                        "tstp": str(item.get("timestamp", "")).replace(
                            " ", "T"
                        ),
                        "energy(kWh/hh)": to_float(
                            item.get("consumption_kwh")
                        ),
                        "price_pence": to_float(
                            item.get("avg_price_pence")
                        ),
                    }
                    for item in records
                ]

                simulation_payload = {
                    "household_id": household_id,
                    "data": simulation_rows,
                    "devices": {},
                }

                self.hourly_chart_data = create_hourly_fallback(records)
                try:
                    hours_response = await client.post(
                        f"{FASTAPI_URL}/simulation/hours",
                        json=simulation_payload,
                    )
                    hours_response.raise_for_status()
                    hours_payload = hours_response.json()
                    parsed_hours = parse_hour_rows(hours_payload)

                    if parsed_hours:
                        self.hours_data = hours_payload
                        self.hourly_chart_data = parsed_hours
                except (httpx.HTTPError, TypeError, ValueError):
                    optional_failures.append("hourly simulation")

                costs_response = await client.post(
                    f"{FASTAPI_URL}/simulation/costs",
                    json=simulation_payload,
                )
                costs_response.raise_for_status()
                costs_payload = costs_response.json()
                self.costs_data = costs_payload
                self.total_consumption_kwh = to_float(
                    costs_payload.get("total_consumption_kwh")
                )
                self.total_cost_pounds = to_float(
                    costs_payload.get("total_cost_pounds")
                )

                carbon_impact = costs_payload.get("carbon_impact") or {}
                if isinstance(carbon_impact, dict):
                    self.carbon_kg = to_float(
                        carbon_impact.get("carbon_kg")
                    )

                try:
                    recommendations_response = await client.post(
                        f"{FASTAPI_URL}/recommendations/load-shift",
                        json=simulation_payload,
                    )
                    recommendations_response.raise_for_status()
                    recommendations_payload = recommendations_response.json()

                    prices = [
                        to_float(item.get("avg_price_pence"))
                        for item in records
                    ]

                    print("\n--- RECOMMENDATION DEBUG ---")
                    print("Household:", household_id)
                    print("Tariff:", self.household_tariff)
                    print("Minimum price:", min(prices) if prices else None)
                    print("Maximum price:", max(prices) if prices else None)
                    print("Recommendation response:", recommendations_payload)
                    print("--------------------------------\n")

                    self.recommendations_data = recommendations_payload
                    self.total_savings_pounds = to_float(
                        recommendations_payload.get("total_savings_pounds")
                    )
                    recommendations = extract_list(
                        recommendations_payload,
                        ("recommendations", "data", "items"),
                    )

                    self.recommendation_cards = [
                        {
                            "icon": str(item.get("icon", "⚡")),
                            "device": translate_device(
                                item.get("device", "Appliance")
                            ).title(),
                            "time_shift": (
                                f"{item.get('current_hour', '—')} → "
                                f"{item.get('recommended_hour', '—')}"
                            ),
                            "saving": (
                                "£"
                                f"{to_float(item.get('estimated_savings_pounds')):.2f}"
                            ),
                            "carbon": (
                                f"{to_float(item.get('carbon_reduction_kg')):.2f} "
                                "kg CO₂"
                            ),
                        }
                        for item in recommendations
                    ]

                    if recommendations:
                        top_recommendation = max(
                            recommendations,
                            key=lambda item: to_float(
                                item.get("estimated_savings_pounds")
                            ),
                        )
                        device = translate_device(
                            top_recommendation.get("device")
                        )
                        self.best_action_device = device.strip().title()

                        current_hour = top_recommendation.get(
                            "current_hour", "the current time"
                        )
                        recommended_hour = top_recommendation.get(
                            "recommended_hour", "a cheaper period"
                        )
                        saving = to_float(
                            top_recommendation.get(
                                "estimated_savings_pounds"
                            )
                        )

                        self.best_action_title = (
                            f"Run your {device} at {recommended_hour}"
                        )
                        self.best_action_message = (
                            f"Move it from {current_hour} to "
                            f"{recommended_hour} to save approximately "
                            f"£{saving:.2f}."
                        )
                    else:
                        self.best_action_device = ""
                        self.best_action_title = (
                            "No load-shifting savings found"
                        )
                        self.best_action_message = (
                            "The selected period does not contain a useful "
                            "lower-cost appliance shift."
                        )
                except (httpx.HTTPError, TypeError, ValueError):
                    self.best_action_device = ""
                    self.best_action_title = "Recommendations unavailable"
                    self.best_action_message = (
                        "Consumption and cost data loaded, but the "
                        "recommendation service could not be reached."
                    )
                    optional_failures.append("recommendations")

                try:
                    anomaly_response = await client.post(
                        f"{FASTAPI_URL}/alerts/anomaly",
                        json=simulation_payload,
                    )
                    anomaly_response.raise_for_status()
                    anomaly_payload = anomaly_response.json()
                    self.anomaly_data = anomaly_payload
                    self.anomaly_detected = bool(
                        anomaly_payload.get("anomaly_detected", False)
                    )
                    self.anomaly_summary = (
                        "We detected unusual energy use. A device may "
                        "have been left running."
                        if self.anomaly_detected
                        else "No unusual energy use was detected."
                    )

                    anomalies = extract_list(
                        anomaly_payload,
                        ("anomalies", "data", "items"),
                    )
                    self.total_anomaly_count = len(anomalies)
                    self.anomaly_cards = [
                        {
                            "timestamp": str(
                                item.get("timestamp", "Unknown time")
                            ).replace("T", " ")[:16],
                            "usage": (
                                "Expected "
                                f"{to_float(item.get('expected_kwh')):.2f} kWh "
                                "· Actual "
                                f"{to_float(item.get('actual_kwh')):.2f} kWh"
                            ),
                            "deviation": (
                                f"{to_float(item.get('deviation_percent')):.1f}% "
                                "above expected"
                            ),
                        }
                        for item in anomalies[:20]
                    ]
                except (httpx.HTTPError, TypeError, ValueError):
                    self.anomaly_summary = (
                        "Anomaly detection is currently unavailable."
                    )
                    optional_failures.append("anomaly detection")

                try:
                    coach_response = await client.get(
                        f"{FASTAPI_URL}/coach/context",
                        params={"household_id": household_id},
                    )
                    coach_response.raise_for_status()
                    coach_payload = coach_response.json()
                    self.coach_context_data = coach_payload
                    self.coach_prompt_context = str(
                        coach_payload.get("prompt_context") or ""
                    )
                    self.coach_context_available = bool(
                        self.coach_prompt_context
                        or coach_payload.get("weekly_summary")
                    )
                    self.coach_message = create_coach_message(
                        coach_payload,
                        selected_consumption_kwh=(
                            self.total_consumption_kwh
                        ),
                        selected_cost_pounds=self.total_cost_pounds,
                        fallback_recommendation=(
                            self.best_action_message
                        ),
                        anomaly_detected=self.anomaly_detected,
                    )
                except (httpx.HTTPError, TypeError, ValueError):
                    self.coach_context_available = False
                    self.coach_message = create_coach_message(
                        {},
                        selected_consumption_kwh=(
                            self.total_consumption_kwh
                        ),
                        selected_cost_pounds=self.total_cost_pounds,
                        fallback_recommendation=(
                            self.best_action_message
                        ),
                        anomaly_detected=self.anomaly_detected,
                    )
                    optional_failures.append("coach context")

                self.coach_messages = [
                    {
                        "role": "assistant",
                        "content": self.coach_message,
                    }
                ]

                self.dashboard_loaded = True
                self.backend_online = True
                self.backend_status = "Services online"

                if self.tour_seen != "true":
                    self.tour_step = 0
                    self.tour_open = True

                if optional_failures:
                    self.partial_data_message = (
                        "Dashboard loaded with fallback data for: "
                        + ", ".join(optional_failures)
                        + "."
                    )

        except httpx.HTTPStatusError as exc:
            self.error_message = (
                "Backend returned error "
                f"{exc.response.status_code}: "
                f"{exc.response.text[:200]}"
            )
        except httpx.RequestError:
            self.backend_online = False
            self.backend_status = "Backend unavailable"
            self.error_message = (
                "Could not connect to the FastAPI backend on port 8000."
            )
        except (TypeError, ValueError, KeyError) as exc:
            self.error_message = (
                f"The backend response could not be processed: {exc}"
            )
        finally:
            self.is_loading = False