import reflex as rx

from ..components.navbar import navbar
from ..state import DashboardState
from ..styles import (
    ACCENT,
    BACKGROUND,
    BORDER,
    MUTED,
    PAGE_CONTAINER,
    PRIMARY,
    SOFT_GREEN,
    SURFACE,
)


def metric_card(
    label: str,
    value,
    detail,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                label,
                color=MUTED,
                font_size="0.9rem",
            ),
            rx.heading(
                value,
                size="7",
                color=PRIMARY,
            ),
            rx.text(
                detail,
                color=ACCENT,
                font_size="0.85rem",
                font_weight="600",
            ),
            align="start",
            spacing="3",
        ),
        flex="1 1 210px",
        padding="1.6rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="18px",
    )

def energy_chart(
    title: str,
    subtitle: str,
    data,
    line_name: str,
    line_color: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                title,
                size="6",
                color=PRIMARY,
            ),
            rx.text(
                subtitle,
                color=MUTED,
            ),
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="4 4",
                    stroke="#DDE7E4",
                ),
                rx.recharts.x_axis(
                    data_key="timestamp",
                    min_tick_gap=35,
                ),
                rx.recharts.y_axis(),
                rx.recharts.graphing_tooltip(),
                rx.recharts.line(
                    data_key="value",
                    name=line_name,
                    stroke=line_color,
                    stroke_width=3,
                    dot=False,
                    type_="monotone",
                ),
                data=data,
                width="100%",
                height=320,
                margin={
                    "top": 10,
                    "right": 20,
                    "left": 0,
                    "bottom": 10,
                },
            ),
            align="start",
            spacing="4",
        ),
        width="100%",
        padding="2rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="20px",
    )


def recommendation_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                item["icon"],
                font_size="1.8rem",
            ),
            rx.heading(
                item["device"],
                size="5",
                color=PRIMARY,
            ),
            rx.text(
                item["time_shift"],
                color=MUTED,
                font_weight="600",
            ),
            rx.heading(
                item["saving"],
                size="6",
                color=ACCENT,
            ),
            rx.text(
                item["carbon"],
                color=MUTED,
                font_size="0.9rem",
            ),
            align="start",
            spacing="3",
        ),
        flex="1 1 220px",
        padding="1.5rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="18px",
    )


def anomaly_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                item["timestamp"],
                color=PRIMARY,
                font_weight="700",
            ),
            rx.text(
                item["usage"],
                color=MUTED,
            ),
            rx.text(
                item["deviation"],
                color="#C2413B",
                font_weight="700",
            ),
            align="start",
            spacing="2",
        ),
        width="100%",
        padding="1rem",
        background="#FFF7F6",
        border="1px solid #F2CBC7",
        border_radius="12px",
    )

def dashboard() -> rx.Component:
    return rx.box(
        navbar(),

        # Page heading
        rx.box(
            rx.vstack(
                rx.text(
                    "PERSONALISED ENERGY INSIGHTS",
                    color=ACCENT,
                    font_size="0.8rem",
                    font_weight="700",
                    letter_spacing="0.12em",
                ),
                rx.heading(
                    "Your energy dashboard",
                    size="9",
                    color=PRIMARY,
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    (
                        "Explore your consumption and discover practical "
                        "opportunities to reduce your bill."
                    ),
                    color=MUTED,
                    font_size="1.1rem",
                ),
                align="start",
                spacing="4",
                **PAGE_CONTAINER,
            ),
            padding="4.5rem 0 3rem",
            background=BACKGROUND,
        ),

        # Dashboard filters
        rx.box(
            rx.vstack(
                rx.text(
                    "Dashboard settings",
                    color=PRIMARY,
                    font_weight="700",
                    font_size="1.05rem",
                ),

                rx.flex(
                    # Household ID
                    rx.vstack(
                        rx.text(
                            "Household ID",
                            color=PRIMARY,
                        ),
                        rx.input(
                            value=DashboardState.household_id,
                            on_change=DashboardState.update_household_id,
                            placeholder="Example: MAC001074",
                            width="100%",
                        ),
                        align="start",
                        flex="1 1 220px",
                    ),

                    # Start date
                    rx.vstack(
                        rx.text(
                            "Start date",
                            color=PRIMARY,
                        ),
                        rx.input(
                            type="date",
                            value=DashboardState.start_date,
                            on_change=DashboardState.update_start_date,
                            min="2012-11-01",
                            max="2014-02-28",
                            width="100%",
                        ),
                        align="start",
                        flex="1 1 200px",
                    ),

                    # End date
                    rx.vstack(
                        rx.text(
                            "End date",
                            color=PRIMARY,
                        ),
                        rx.input(
                            type="date",
                            value=DashboardState.end_date,
                            on_change=DashboardState.update_end_date,
                            min="2012-11-01",
                            max="2014-02-28",
                            width="100%",
                        ),
                        align="start",
                        flex="1 1 200px",
                    ),

                    # Load button
                    rx.button(
                        "Load dashboard",
                        on_click=DashboardState.load_dashboard,
                        loading=DashboardState.is_loading,
                        disabled=DashboardState.is_loading,
                        background=ACCENT,
                        color="white",
                        border_radius="11px",
                        padding="1.35rem 1.6rem",
                        align_self="end",
                        cursor="pointer",
                        _hover={
                            "opacity": "0.9",
                        },
                    ),

                    width="100%",
                    gap="1rem",
                    align="end",
                    flex_wrap="wrap",
                ),

                rx.cond(
                    DashboardState.dashboard_loaded,
                    rx.vstack(
                        # History chart
                        energy_chart(
                            "Consumption history",
                            "Half-hourly electricity usage for the selected period.",
                            DashboardState.history_chart_data,
                            "Consumption (kWh)",
                            ACCENT,
                        ),

                        # Forecast chart
                        energy_chart(
                            "Next 24-hour forecast",
                            "Predicted consumption generated by the forecast service.",
                            DashboardState.forecast_chart_data,
                            "Forecast (kWh)",
                            "#E5A11A",
                        ),

                        # Anomaly section
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Consumption anomalies",
                                    size="6",
                                    color=PRIMARY,
                                ),

                                rx.cond(
                                    DashboardState.anomaly_detected,

                                    rx.accordion.root(
                                        rx.accordion.item(
                                            value="anomaly-details",

                                            header=rx.hstack(
                                                rx.vstack(
                                                    rx.text(
                                                        DashboardState.anomaly_count_text,
                                                        color=PRIMARY,
                                                        font_weight="700",
                                                    ),
                                                    rx.text(
                                                        "Click to review unusual consumption periods.",
                                                        color=MUTED,
                                                        font_size="0.9rem",
                                                    ),
                                                    align="start",
                                                    spacing="1",
                                                ),

                                                rx.badge(
                                                    "View details",
                                                    color_scheme="red",
                                                    variant="soft",
                                                ),

                                                width="100%",
                                                justify="between",
                                                align="center",
                                            ),

                                            content=rx.vstack(
                                                rx.callout(
                                                    DashboardState.anomaly_summary,
                                                    color_scheme="red",
                                                    width="100%",
                                                ),

                                                rx.box(
                                                    rx.vstack(
                                                        rx.foreach(
                                                            DashboardState.anomaly_cards,
                                                            anomaly_card,
                                                        ),
                                                        width="100%",
                                                        spacing="3",
                                                    ),
                                                    width="100%",
                                                    max_height="480px",
                                                    overflow_y="auto",
                                                ),

                                                rx.cond(
                                                    DashboardState.total_anomaly_count > 20,
                                                    rx.text(
                                                        "Showing the first 20 anomalies.",
                                                        color=MUTED,
                                                        font_size="0.85rem",
                                                    ),
                                                    rx.fragment(),
                                                ),

                                                width="100%",
                                                spacing="4",
                                                padding_top="1rem",
                                            ),

                                            color_scheme="red",
                                            variant="surface",
                                        ),

                                        type="single",
                                        collapsible=True,
                                        width="100%",
                                    ),

                                    rx.callout(
                                        "No unusual energy consumption was detected.",
                                        color_scheme="green",
                                        width="100%",
                                    ),
                                ),

                                align="start",
                                spacing="4",
                            ),
                            width="100%",
                            padding="2rem",
                            background=SURFACE,
                            border=f"1px solid {BORDER}",
                            border_radius="20px",
                        ),
                        
                        # Recommendation cards
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Personalised recommendations",
                                    size="6",
                                    color=PRIMARY,
                                ),
                                rx.text(
                                    "Practical appliance shifts based on your tariff.",
                                    color=MUTED,
                                ),

                                rx.cond(
                                    DashboardState.recommendation_cards.length() > 0,
                                    rx.flex(
                                        rx.foreach(
                                            DashboardState.recommendation_cards,
                                            recommendation_card,
                                        ),
                                        width="100%",
                                        gap="1rem",
                                        flex_wrap="wrap",
                                    ),
                                    rx.callout(
                                        "No useful appliance shifts were found.",
                                        color_scheme="blue",
                                        width="100%",
                                    ),
                                ),

                                align="start",
                                spacing="4",
                            ),
                            width="100%",
                            padding="2rem",
                            background=SURFACE,
                            border=f"1px solid {BORDER}",
                            border_radius="20px",
                        ),

                        width="100%",
                        spacing="6",
                    ),
                    rx.fragment(),
                ),

                # Error message
                rx.cond(
                    DashboardState.error_message != "",
                    rx.callout(
                        DashboardState.error_message,
                        color_scheme="red",
                        width="100%",
                    ),
                    rx.fragment(),
                ),

                # Success message
                rx.cond(
                    DashboardState.dashboard_loaded,
                    rx.callout(
                        "Energy data loaded successfully.",
                        color_scheme="green",
                        width="100%",
                    ),
                    rx.fragment(),
                ),

                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="2rem 0",
            background=SURFACE,
            border_y=f"1px solid {BORDER}",
        ),

        # Dashboard content
        rx.box(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.text(
                            "BEST ACTION TODAY",
                            color=ACCENT,
                            font_size="0.8rem",
                            font_weight="700",
                            letter_spacing="0.1em",
                        ),

                        rx.cond(
                            DashboardState.dashboard_loaded,
                            rx.heading(
                                DashboardState.best_action_title,
                                size="6",
                                color=PRIMARY,
                            ),
                            rx.heading(
                                (
                                    "Load a household to receive "
                                    "personalised advice"
                                ),
                                size="6",
                                color=PRIMARY,
                            ),
                        ),

                        rx.cond(
                            DashboardState.dashboard_loaded,
                            rx.text(
                                DashboardState.best_action_message,
                                color=MUTED,
                            ),
                            rx.text(
                                (
                                    "Volti will identify your clearest saving "
                                    "opportunity and display it here."
                                ),
                                color=MUTED,
                            ),
                        ),

                        align="start",
                        spacing="4",
                    ),
                    width="100%",
                    padding="2rem",
                    background=SOFT_GREEN,
                    border=f"1px solid {BORDER}",
                    border_radius="20px",
                ),

                rx.flex(
                    metric_card(
                        "Consumption",
                        DashboardState.total_consumption_text,
                        "Selected period",
                    ),

                    metric_card(
                        "Estimated cost",
                        DashboardState.total_cost_text,
                        "Selected period",
                    ),

                    metric_card(
                        "Saving potential",
                        DashboardState.total_savings_text,
                        DashboardState.recommendation_count_text,
                    ),

                    metric_card(
                        "Carbon impact",
                        DashboardState.carbon_text,
                        "Estimated CO₂ footprint",
                    ),
                    width="100%",
                    gap="1rem",
                    flex_wrap="wrap",
                ),

                spacing="6",
                **PAGE_CONTAINER,
            ),
            padding="3rem 0 5rem",
            background=BACKGROUND,
        ),

        min_height="100vh",
        background=BACKGROUND,
    )