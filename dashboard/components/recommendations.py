from typing import Any

import streamlit as st


def render_recommendations(
    recommendations_data: dict[str, Any],
) -> None:
    st.markdown("### Saving Recommendations")

    recommendations = recommendations_data.get(
        "recommendations",
        [],
    )

    total_savings = recommendations_data.get(
        "total_savings_pounds",
        0.0,
    )

    if not recommendations:
        st.info(
            "No load-shifting recommendations are available."
        )
        st.divider()
        return

    st.caption(
        f"Estimated total saving potential: £{total_savings:.2f}"
    )

    # Display a maximum of three cards per row.
    for start_index in range(0, len(recommendations), 3):
        row_items = recommendations[
            start_index:start_index + 3
        ]

        columns = st.columns(len(row_items))

        for column, item in zip(columns, row_items):
            with column:
                device = item.get("device", "Unknown device")
                icon = item.get("icon", "⚡")
                current_hour = item.get(
                    "current_hour",
                    "Unknown",
                )
                recommended_hour = item.get(
                    "recommended_hour",
                    "Unknown",
                )
                savings = item.get(
                    "estimated_savings_pounds",
                    0.0,
                )
                saving_percent = item.get(
                    "saving_percent",
                    0.0,
                )
                carbon_reduction = item.get(
                    "carbon_reduction_kg",
                    0.0,
                )

                with st.container(border=True):
                    st.markdown(f"#### {icon} {device}")
                    st.write(
                        f"**Schedule:** "
                        f"{current_hour} → {recommended_hour}"
                    )
                    st.metric(
                        "Estimated Saving",
                        f"£{savings:.2f}",
                        delta=f"{saving_percent:.1f}%",
                    )
                    st.caption(
                        f"Carbon reduction: "
                        f"{carbon_reduction:.3f} kg CO₂"
                    )

    st.divider()