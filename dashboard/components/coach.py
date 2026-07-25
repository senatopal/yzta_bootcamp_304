from typing import Any

import streamlit as st

device_names = {
    "Çamaşır Makinesi": "Washing Machine",
    "Bulaşık Makinesi": "Dishwasher",
    "Kurutma Makinesi": "Tumble Dryer",
    "Elektrikli Araç Şarjı": "Electric Vehicle Charging",
}

def render_coach(coach_context: dict[str, Any]) -> None:
    st.markdown("### Volti Energy Coach")

    weekly_summary = coach_context.get("weekly_summary")
    recommendations = coach_context.get("recommendations", [])
    anomalies = coach_context.get("anomalies", [])

    if weekly_summary is None:
        with st.chat_message("assistant"):
            st.write(
                "There is not enough consumption history yet. "
                "Once more data is available, I will provide personalised "
                "energy-saving advice."
            )

        st.divider()
        return

    total_consumption = weekly_summary.get(
        "total_consumption_kwh",
        0.0,
    )
    total_cost = weekly_summary.get(
        "total_cost_pounds",
        0.0,
    )

    message_parts = [
        (
            f"Your total consumption over the last seven days was "
            f"**{total_consumption:.2f} kWh**, costing approximately "
            f"**£{total_cost:.2f}**."
        )
    ]

    if anomalies:
        latest_anomaly = anomalies[0]
        anomaly_time = latest_anomaly.get(
            "timestamp",
            "an unknown time",
        )

        message_parts.append(
            f"An unusual consumption spike was detected at "
            f"**{anomaly_time}**. Please check whether any appliance "
            f"was left running."
        )

    if recommendations:
        top_recommendation = recommendations[0]
        
        raw_device = top_recommendation.get(
            "device",
            "an appliance",
        )

        device = device_names.get(
            raw_device,
            raw_device,
        )
        
        current_hour = top_recommendation.get(
            "current_hour",
            "the current time",
        )
        recommended_hour = top_recommendation.get(
            "recommended_hour",
            "an off-peak time",
        )
        savings = top_recommendation.get(
            "estimated_savings_pounds",
            0.0,
        )

        message_parts.append(
            f"Moving **{device}** from **{current_hour}** to "
            f"**{recommended_hour}** could save approximately "
            f"**£{savings:.2f}**."
        )
    elif not anomalies:
        message_parts.append(
            "Your current consumption pattern looks efficient, "
            "and no urgent changes are recommended."
        )

    with st.chat_message("assistant"):
        st.markdown(" ".join(message_parts))

    st.divider()