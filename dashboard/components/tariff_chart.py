from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_tariff_chart(consumption: dict[str, Any]) -> None:
    st.markdown("### Electricity Tariff")

    tariff_df = pd.DataFrame(consumption.get("data", []))

    if tariff_df.empty or "avg_price_pence" not in tariff_df.columns:
        st.info("No tariff data is available.")
        st.divider()
        return

    tariff_df["timestamp"] = pd.to_datetime(
        tariff_df["timestamp"],
        errors="coerce",
    )

    tariff_df["avg_price_pence"] = pd.to_numeric(
        tariff_df["avg_price_pence"],
        errors="coerce",
    )

    tariff_df = (
        tariff_df
        .dropna(subset=["timestamp", "avg_price_pence"])
        .sort_values("timestamp")
    )

    if tariff_df.empty:
        st.info("No valid tariff data is available.")
        st.divider()
        return

    bar_colors = []

    for price in tariff_df["avg_price_pence"]:
        if price < 10:
            bar_colors.append("#2ecc71")
        elif price < 22:
            bar_colors.append("#f39c12")
        else:
            bar_colors.append("#e74c3c")

    fig = go.Figure(
        go.Bar(
            x=tariff_df["timestamp"],
            y=tariff_df["avg_price_pence"],
            marker_color=bar_colors,
            hovertemplate=(
                "%{x|%d %b %H:%M}<br>"
                "%{y:.2f} p/kWh<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Price (pence/kWh)",
        height=360,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
    )

    st.caption(
        "🟢 Low price · 🟠 Medium price · 🔴 High price"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()