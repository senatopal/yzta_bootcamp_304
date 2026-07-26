from datetime import date, datetime, time

import streamlit as st

from dashboard.api.client import APIClientError
from dashboard.components.anomaly import render_anomaly
from dashboard.components.coach import render_coach
from dashboard.components.consumption_chart import render_consumption_chart
from dashboard.components.recommendations import render_recommendations
from dashboard.components.summary import render_summary
from dashboard.components.tariff_chart import render_tariff_chart
from dashboard.services.dashboard_service import dashboard_service


@st.cache_data(ttl=60, show_spinner=False)
def load_dashboard_data(
    household_id: str,
    forecast_days: int,
    start_date: date,
    end_date: date,
):
    return dashboard_service.get_dashboard_data(
        household_id=household_id,
        period="half-hourly",
        forecast_days=forecast_days,
        start_date=datetime.combine(
            start_date,
            time.min,
        ).isoformat(),
        end_date=datetime.combine(
            end_date,
            time.max,
        ).isoformat(),
    )


st.html(
    """
    <div class="page-header">
        <span class="volti-eyebrow">
            PERSONALISED ENERGY INSIGHTS
        </span>

        <h1>Your energy dashboard</h1>

        <p>
            Understand your consumption and discover practical
            opportunities to reduce your bill.
        </p>
    </div>
    """
)


with st.sidebar:
    st.markdown("### Dashboard settings")

    household_id = st.text_input(
        "Household ID",
        value="MAC000002",
        placeholder="Example: MAC000002",
    )

    start_date = st.date_input(
        "Start date",
        value=date(2013, 11, 1),
    )

    end_date = st.date_input(
        "End date",
        value=date(2013, 11, 7),
    )

    forecast_days = st.slider(
        "Forecast days",
        min_value=1,
        max_value=7,
        value=1,
    )

    load_button = st.button(
        "Load dashboard",
        type="primary",
        use_container_width=True,
    )


if load_button:
    cleaned_household_id = household_id.strip()

    if not cleaned_household_id:
        st.warning("Please enter a household ID.")
        st.stop()

    if start_date > end_date:
        st.warning("Start date cannot be later than end date.")
        st.stop()

    try:
        with st.spinner("Analysing your energy data..."):
            st.session_state["dashboard_data"] = load_dashboard_data(
                household_id=cleaned_household_id,
                forecast_days=forecast_days,
                start_date=start_date,
                end_date=end_date,
            )

    except APIClientError as exc:
        st.error(str(exc))
        st.stop()


dashboard_data = st.session_state.get("dashboard_data")

if dashboard_data is None:
    st.html(
        """
        <section class="dashboard-empty-state">
            <div class="empty-state-icon">⚡</div>

            <h2>See where your energy can work smarter</h2>

            <p>
                Choose a household and date range from the sidebar,
                then load the dashboard to view personalised insights.
            </p>
        </section>
        """
    )

    st.stop()


render_summary(
    dashboard_data["costs"],
    dashboard_data["recommendations"],
)

render_anomaly(
    dashboard_data["anomaly"],
)

render_consumption_chart(
    dashboard_data["consumption"],
    dashboard_data["forecast"],
    dashboard_data["anomaly"],
)

render_tariff_chart(
    dashboard_data["consumption"],
)

render_recommendations(
    dashboard_data["recommendations"],
)

render_coach(
    dashboard_data["coach_context"],
)