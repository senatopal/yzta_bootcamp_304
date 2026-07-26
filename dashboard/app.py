import streamlit as st
from datetime import date, datetime, time

from dashboard.api.client import APIClientError
from dashboard.services.dashboard_service import dashboard_service

from dashboard.components.summary import render_summary
from dashboard.components.anomaly import render_anomaly
from dashboard.components.consumption_chart import render_consumption_chart
from dashboard.components.tariff_chart import render_tariff_chart
from dashboard.components.recommendations import render_recommendations
from dashboard.components.coach import render_coach


st.set_page_config(
    page_title="Volti",
    page_icon="⚡",
    layout="wide",
)

st.title("Volti — Your Energy Saving Coach")
st.caption("Discover saving opportunities using your smart meter data.")


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


household_id = st.sidebar.text_input(
    "Household ID",
    value="MAC000002",
)

forecast_days = st.sidebar.slider(
    "Forecast days",
    min_value=1,
    max_value=7,
    value=1,
)

load_button = st.sidebar.button(
    "Load dashboard",
    type="primary",
)

start_date = st.sidebar.date_input(
    "Start date",
    value=date(2013, 11, 1),
)

end_date = st.sidebar.date_input(
    "End date",
    value=date(2013, 11, 7),
)


if load_button:
    if not household_id.strip():
        st.warning("Please enter a household ID.")
        st.stop()

    if start_date > end_date:
        st.warning("Start date cannot be later than end date.")
        st.stop()

    try:
        with st.spinner("Loading energy data..."):
            st.session_state["dashboard_data"] = load_dashboard_data(
                household_id.strip(),
                forecast_days,
                start_date,
                end_date,
            )

    except APIClientError as exc:
        st.error(str(exc))
        st.stop()


dashboard_data = st.session_state.get("dashboard_data")

if dashboard_data is None:
    st.info("Select a household and click **Load dashboard**.")
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