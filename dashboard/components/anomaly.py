from typing import Any

import streamlit as st


def render_anomaly(anomaly: dict[str, Any]) -> None:
    anomaly_detected = anomaly.get("anomaly_detected", False)
    message = anomaly.get(
        "message",
        "No anomaly information is available.",
    )

    if not anomaly_detected:
        st.success(f"{message}")
        st.divider()
        return

    anomalies = anomaly.get("anomalies", [])

    st.error(f"{message}")

    for item in anomalies:
        timestamp = item.get("timestamp", "Unknown time")
        expected = item.get("expected_kwh", 0.0)
        actual = item.get("actual_kwh", 0.0)
        deviation = item.get("deviation_percent", 0.0)

        st.warning(
            f"**Time:** {timestamp}  \n"
            f"**Expected:** {expected:.2f} kWh  \n"
            f"**Actual:** {actual:.2f} kWh  \n"
            f"**Deviation:** {deviation:.1f}%"
        )

    st.divider()