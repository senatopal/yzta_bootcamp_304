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


def hourly_chart(data) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "Hourly energy breakdown",
                        size="6",
                        color=PRIMARY,
                    ),
                    rx.text(
                        (
                            "Total consumption grouped by hour for "
                            "the selected period."
                        ),
                        color=MUTED,
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.badge(
                    "Simulation hours",
                    color_scheme="teal",
                    variant="soft",
                ),
                width="100%",
                justify="between",
                align="center",
            ),
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="4 4",
                    stroke="#DDE7E4",
                ),
                rx.recharts.x_axis(
                    data_key="hour",
                    min_tick_gap=18,
                ),
                rx.recharts.y_axis(),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(
                    data_key="consumption",
                    name="Consumption (kWh)",
                    fill=ACCENT,
                    radius=[6, 6, 0, 0],
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


def floating_coach() -> rx.Component:
    """Floating Volti coach button and expandable popup."""
    return rx.cond(
        DashboardState.dashboard_loaded,
        rx.box(
            rx.cond(
                DashboardState.coach_open,
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.image(
                                    src="/volti_koc_akilli_onerme.png",
                                    width="155px",
                                    height="155px",
                                    object_fit="contain",
                                    object_position="center",
                                ),
                                width="170px",
                                height="170px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                flex_shrink="0",
                            ),
                            rx.vstack(
                                rx.text(
                                    "VOLTI ENERGY COACH",
                                    color=ACCENT,
                                    font_size="0.78rem",
                                    font_weight="700",
                                    letter_spacing="0.12em",
                                ),
                                rx.heading(
                                    "Your energy assistant",
                                    size="7",
                                    color=PRIMARY,
                                ),
                                align="start",
                                justify="center",
                                spacing="2",
                                flex="1",
                                height="170px",
                            ),
                            rx.button(
                                "×",
                                on_click=DashboardState.toggle_coach,
                                background="transparent",
                                color=MUTED,
                                font_size="1.9rem",
                                line_height="1",
                                padding="0",
                                min_width="auto",
                                height="auto",
                                cursor="pointer",
                                align_self="start",
                                aria_label="Close Volti Energy Coach",
                            ),
                            width="100%",
                            justify="between",
                            align="center",
                            spacing="4",
                        ),
                        rx.divider(),
                        rx.text(
                            DashboardState.coach_message,
                            color=MUTED,
                            line_height="1.7",
                            font_size="0.97rem",
                        ),
                        rx.cond(
                            DashboardState.coach_context_available,
                            rx.badge(
                                "Personalised insight",
                                color_scheme="green",
                                variant="soft",
                            ),
                            rx.badge(
                                "Dashboard insight",
                                color_scheme="gray",
                                variant="soft",
                            ),
                        ),
                        align="start",
                        spacing="4",
                    ),
                    width="min(560px, calc(100vw - 32px))",
                    max_height="min(680px, calc(100vh - 150px))",
                    overflow_y="auto",
                    padding="1.55rem",
                    margin_bottom="1rem",
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="26px",
                    box_shadow="0 20px 56px rgba(22, 53, 76, 0.22)",
                ),
                rx.fragment(),
            ),

            rx.button(
                rx.box(
                    rx.image(
                        src="/volti_koc.png",
                        width="140px",
                        height="140px",
                        object_fit="contain",
                        object_position="center bottom",
                        position="absolute",
                        left="50%",
                        bottom="-10px",
                        transform="translateX(-50%)",
                        transform_origin="center bottom",
                        pointer_events="none",
                    ),
                    width="100%",
                    height="100%",
                    position="relative",
                    overflow="visible",
                ),
                on_click=DashboardState.toggle_coach,
                width="104px",
                height="104px",
                padding="0",
                background=SOFT_GREEN,
                border=f"4px solid {SURFACE}",
                border_radius="50%",
                box_shadow="0 16px 38px rgba(22, 53, 76, 0.24)",
                cursor="pointer",
                overflow="visible",
                aria_label="Open Volti Energy Coach",
                _hover={
                    "transform": "translateY(-4px)",
                    "box_shadow": "0 20px 46px rgba(22, 53, 76, 0.30)",
                },
                transition="all 0.2s ease",
            ),

            position="fixed",
            right="24px",
            bottom="24px",
            z_index="1000",
            display="flex",
            flex_direction="column",
            align_items="flex-end",
            overflow="visible",
        ),
        rx.fragment(),
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
                rx.cond(
                    DashboardState.backend_online,
                    rx.badge(
                        DashboardState.backend_status,
                        color_scheme="green",
                        variant="soft",
                        size="2",
                    ),
                    rx.badge(
                        DashboardState.backend_status,
                        color_scheme="red",
                        variant="soft",
                        size="2",
                    ),
                ),
                align="start",
                spacing="4",
                **PAGE_CONTAINER,
            ),
            padding="4.5rem 0 3rem",
            background=BACKGROUND,
        ),

        # Dashboard filters and data sections
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
                            height="42px",
                        ),
                        rx.text(
                            DashboardState.household_count_text,
                            color=MUTED,
                            font_size="0.8rem",
                            min_height="20px",
                        ),
                        align="start",
                        spacing="2",
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
                            height="42px",
                        ),
                        rx.text(
                            "Placeholder",
                            visibility="hidden",
                            font_size="0.8rem",
                            min_height="20px",
                        ),
                        align="start",
                        spacing="2",
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
                            height="42px",
                        ),
                        rx.text(
                            "Placeholder",
                            visibility="hidden",
                            font_size="0.8rem",
                            min_height="20px",
                        ),
                        align="start",
                        spacing="2",
                        flex="1 1 200px",
                    ),

                    # Load button
                    rx.vstack(
                        rx.text(
                            "Action",
                            visibility="hidden",
                        ),
                        rx.button(
                            "Load dashboard",
                            on_click=DashboardState.load_dashboard,
                            loading=DashboardState.is_loading,
                            disabled=DashboardState.is_loading,
                            background=ACCENT,
                            color="white",
                            border_radius="11px",
                            height="42px",
                            padding="0 1.6rem",
                            cursor="pointer",
                            _hover={"opacity": "0.9"},
                        ),
                        rx.text(
                            "Placeholder",
                            visibility="hidden",
                            font_size="0.8rem",
                            min_height="20px",
                        ),
                        align="start",
                        spacing="2",
                        flex_shrink="0",
                    ),

                    width="100%",
                    gap="1rem",
                    align="start",
                    flex_wrap="wrap",
                ),
                rx.cond(
                    DashboardState.error_message != "",
                    rx.callout(
                        DashboardState.error_message,
                        color_scheme="red",
                        width="100%",
                    ),
                    rx.fragment(),
                ),

                rx.cond(
                    DashboardState.dashboard_loaded,
                    rx.callout(
                        "Energy data loaded successfully.",
                        color_scheme="green",
                        width="100%",
                    ),
                    rx.fragment(),
                ),

                rx.cond(
                    DashboardState.dashboard_loaded,
                    rx.vstack(
                        energy_chart(
                            "Consumption history",
                            (
                                "Half-hourly electricity usage for "
                                "the selected period."
                            ),
                            DashboardState.history_chart_data,
                            "Consumption (kWh)",
                            ACCENT,
                        ),

                        energy_chart(
                            "Next 24-hour forecast",
                            (
                                "Predicted consumption generated "
                                "by the forecast service."
                            ),
                            DashboardState.forecast_chart_data,
                            "Forecast (kWh)",
                            "#E5A11A",
                        ),

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
                                                        (
                                                            "Click to review unusual "
                                                            "consumption periods."
                                                        ),
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
                                                    DashboardState.total_anomaly_count
                                                    > 20,
                                                    rx.text(
                                                        (
                                                            "Showing the first "
                                                            "20 anomalies."
                                                        ),
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
                                        (
                                            "No unusual energy consumption "
                                            "was detected."
                                        ),
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

                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Personalised recommendations",
                                    size="6",
                                    color=PRIMARY,
                                ),
                                rx.text(
                                    (
                                        "Practical appliance shifts based "
                                        "on your tariff."
                                    ),
                                    color=MUTED,
                                ),
                                rx.cond(
                                    DashboardState.recommendation_cards.length()
                                    > 0,
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
                                        (
                                            "No useful appliance shifts "
                                            "were found."
                                        ),
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

                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="2rem 0",
            background=SURFACE,
            border_y=f"1px solid {BORDER}",
        ),

        # Dashboard summary
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

        floating_coach(),

        min_height="100vh",
        background=BACKGROUND,
    )