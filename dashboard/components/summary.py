from typing import Any

import streamlit as st


def render_summary(
    costs: dict[str, Any],
    recommendations: dict[str, Any],
) -> None:
    st.markdown("### Daily Overview")

    total_consumption = costs.get("total_consumption_kwh", 0.0)
    total_cost = costs.get("total_cost_pounds", 0.0)
    total_savings = recommendations.get("total_savings_pounds", 0.0)

    carbon_impact = costs.get("carbon_impact", {})
    carbon_kg = carbon_impact.get("carbon_kg", 0.0)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Consumption",
        f"{total_consumption:.2f} kWh",
    )

    col2.metric(
        "Estimated Cost",
        f"£{total_cost:.2f}",
    )

    col3.metric(
        "Saving Potential",
        f"£{total_savings:.2f}",
    )

    col4.metric(
        "Carbon Impact",
        f"{carbon_kg:.2f} kg CO₂",
    )

    st.divider()