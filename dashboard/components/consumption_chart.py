from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_consumption_chart(
    consumption: dict[str, Any],
    forecast: dict[str, Any],
    anomaly: dict[str, Any],
) -> None:
    st.markdown("### Consumption & Forecast")

    consumption_df = pd.DataFrame(consumption.get("data", []))
    forecast_df = pd.DataFrame(forecast.get("data", []))

    if consumption_df.empty and forecast_df.empty:
        st.info("No consumption or forecast data is available.")
        st.divider()
        return

    fig = go.Figure()

    if not consumption_df.empty:
        consumption_df["timestamp"] = pd.to_datetime(
            consumption_df["timestamp"],
            errors="coerce",
        )
        consumption_df = consumption_df.dropna(
            subset=["timestamp"]
        ).sort_values("timestamp")

        fig.add_trace(
            go.Scatter(
                x=consumption_df["timestamp"],
                y=consumption_df["consumption_kwh"],
                mode="lines+markers",
                name="Actual Consumption",
                hovertemplate=(
                    "%{x|%d %b %H:%M}<br>"
                    "%{y:.3f} kWh<extra></extra>"
                ),
            )
        )

    if not forecast_df.empty:
        forecast_df["timestamp"] = pd.to_datetime(
            forecast_df["timestamp"],
            errors="coerce",
        )
        forecast_df = forecast_df.dropna(
            subset=["timestamp"]
        ).sort_values("timestamp")

        fig.add_trace(
            go.Scatter(
                x=forecast_df["timestamp"],
                y=forecast_df["predicted_kwh"],
                mode="lines",
                name="Forecast",
                line={"dash": "dash"},
                hovertemplate=(
                    "%{x|%d %b %H:%M}<br>"
                    "%{y:.3f} kWh<extra></extra>"
                ),
            )
        )

    for item in anomaly.get("anomalies", []):
        timestamp = pd.to_datetime(
            item.get("timestamp"),
            errors="coerce",
        )

        if pd.notna(timestamp):
            fig.add_vline(
                x=timestamp.timestamp() * 1000,
                line_dash="dot",
                annotation_text="Anomaly",
                annotation_position="top",
            )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Consumption (kWh)",
        hovermode="x unified",
        height=420,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()