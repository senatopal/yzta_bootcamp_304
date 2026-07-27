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
            rx.text(label, color=MUTED, font_size="0.9rem"),
            rx.heading(value, size="7", color=PRIMARY),
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
            rx.heading(title, size="6", color=PRIMARY),
            rx.text(subtitle, color=MUTED),
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
            rx.text(item["icon"], font_size="1.8rem"),
            rx.heading(item["device"], size="5", color=PRIMARY),
            rx.text(
                item["time_shift"],
                color=MUTED,
                font_weight="600",
            ),
            rx.heading(item["saving"], size="6", color=ACCENT),
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
            rx.text(item["usage"], color=MUTED),
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


def coach_message_bubble(item) -> rx.Component:
    is_user = item["role"] == "user"

    return rx.hstack(
        rx.box(
            rx.text(
                item["content"],
                color=rx.cond(is_user, "white", PRIMARY),
                font_size="0.92rem",
                line_height="1.65",
                white_space="pre-wrap",
            ),
            max_width="88%",
            padding="0.8rem 1rem",
            background=rx.cond(is_user, ACCENT, "#F2F7F5"),
            border=rx.cond(
                is_user,
                f"1px solid {ACCENT}",
                f"1px solid {BORDER}",
            ),
            border_radius=rx.cond(
                is_user,
                "18px 18px 4px 18px",
                "18px 18px 18px 4px",
            ),
        ),
        width="100%",
        justify=rx.cond(is_user, "end", "start"),
    )


def coach_popup() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.center(
                        rx.image(
                            src="/volti_koc_akilli_onerme.png",
                            width="76px",
                            height="76px",
                            object_fit="contain",
                        ),
                        width="66px",
                        height="66px",
                        overflow="visible",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.heading(
                            "Volti Energy Coach",
                            size="5",
                            color=PRIMARY,
                        ),
                        rx.hstack(
                            rx.box(
                                width="8px",
                                height="8px",
                                border_radius="999px",
                                background="#2FA36B",
                            ),
                            rx.text(
                                "Grounded by household data",
                                color=MUTED,
                                font_size="0.78rem",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.button(
                    "×",
                    on_click=DashboardState.toggle_coach,
                    background="transparent",
                    color=MUTED,
                    font_size="1.45rem",
                    padding="0.25rem 0.5rem",
                    min_width="auto",
                    cursor="pointer",
                    _hover={"color": PRIMARY},
                ),
                width="100%",
                justify="between",
                align="center",
            ),

            rx.box(
                rx.vstack(
                    rx.foreach(
                        DashboardState.coach_messages,
                        coach_message_bubble,
                    ),
                    rx.cond(
                        DashboardState.coach_is_sending,
                        rx.hstack(
                            rx.spinner(size="2"),
                            rx.text(
                                "Volti is analysing your household data…",
                                color=MUTED,
                                font_size="0.85rem",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        rx.fragment(),
                    ),
                    width="100%",
                    align="stretch",
                    spacing="3",
                ),
                width="100%",
                height="330px",
                overflow_y="auto",
                padding="0.25rem 0.25rem 0.5rem",
            ),

            rx.cond(
                DashboardState.coach_error != "",
                rx.callout(
                    DashboardState.coach_error,
                    color_scheme="red",
                    size="1",
                    width="100%",
                ),
                rx.fragment(),
            ),

            rx.vstack(
                rx.input(
                    value=DashboardState.coach_input,
                    on_change=DashboardState.update_coach_input,
                    placeholder="Ask about usage, costs or savings…",
                    width="100%",
                    height="44px",
                    disabled=DashboardState.coach_is_sending,
                ),
                rx.hstack(
                    rx.button(
                        "Clear chat",
                        on_click=DashboardState.clear_coach_chat,
                        background="transparent",
                        color=MUTED,
                        border=f"1px solid {BORDER}",
                        border_radius="10px",
                        cursor="pointer",
                    ),
                    rx.button(
                        "Send",
                        on_click=DashboardState.send_coach_message,
                        loading=DashboardState.coach_is_sending,
                        disabled=DashboardState.coach_is_sending,
                        background=ACCENT,
                        color="white",
                        border_radius="10px",
                        padding="0 1.3rem",
                        cursor="pointer",
                        _hover={"opacity": "0.92"},
                    ),
                    width="100%",
                    justify="between",
                    align="center",
                ),
                width="100%",
                spacing="3",
            ),

            rx.cond(
                DashboardState.coach_model != "",
                rx.text(
                    "Powered by " + DashboardState.coach_model,
                    color=MUTED,
                    font_size="0.72rem",
                    text_align="center",
                    width="100%",
                ),
                rx.text(
                    "AI responses are estimates based on available data.",
                    color=MUTED,
                    font_size="0.72rem",
                    text_align="center",
                    width="100%",
                ),
            ),

            width="100%",
            align="stretch",
            spacing="4",
        ),
        position="fixed",
        right="28px",
        bottom="128px",
        width="400px",
        max_width="calc(100vw - 32px)",
        padding="1.25rem",
        background="rgba(255,255,255,0.98)",
        backdrop_filter="blur(16px)",
        border=f"1px solid {BORDER}",
        border_radius="24px",
        box_shadow="0 24px 70px rgba(22,53,76,0.20)",
        z_index="1100",
    )


def coach_launcher() -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src="/volti_koc.png",
                width="108px",
                height="108px",
                object_fit="contain",
                position="absolute",
                bottom="-8px",
                left="50%",
                transform="translateX(-50%)",
                z_index="2",
                pointer_events="none",
            ),
            rx.box(
                "AI",
                position="absolute",
                top="5px",
                right="4px",
                color="white",
                background=ACCENT,
                border="3px solid white",
                border_radius="999px",
                padding="0.22rem 0.4rem",
                font_size="0.62rem",
                font_weight="800",
                z_index="3",
            ),
            width="88px",
            height="88px",
            border_radius="999px",
            background="#EAF5F2",
            border="6px solid white",
            box_shadow="0 14px 36px rgba(0,0,0,0.14)",
            position="relative",
            overflow="visible",
        ),
        on_click=DashboardState.toggle_coach,
        cursor="pointer",
        position="fixed",
        bottom="28px",
        right="28px",
        z_index="1200",
        aria_label="Open Volti Energy Coach",
    )


def floating_coach() -> rx.Component:
    return rx.cond(
        DashboardState.dashboard_loaded,
        rx.fragment(
            rx.cond(
                DashboardState.coach_open,
                coach_popup(),
                rx.fragment(),
            ),
            coach_launcher(),
        ),
        rx.fragment(),
    )



def dashboard_hero_mascot() -> rx.Component:
    """Small branded illustration for the dashboard introduction."""
    return rx.center(
        rx.box(
            # Soft halo behind the transparent PNG.
            rx.box(
                position="absolute",
                inset="20px 10px 8px",
                background=(
                    "radial-gradient(circle at 50% 45%, "
                    "rgba(255,255,255,0.96) 0%, "
                    "rgba(228,243,238,0.82) 58%, "
                    "rgba(228,243,238,0.18) 100%)"
                ),
                border="1px solid rgba(22,135,126,0.10)",
                border_radius="42% 58% 46% 54% / 56% 44% 56% 44%",
                box_shadow="0 18px 42px rgba(22,53,76,0.07)",
                z_index="0",
            ),
            rx.image(
                src="/mascots/analysing.png",
                width="235px",
                height="235px",
                object_fit="contain",
                position="relative",
                z_index="2",
                transform="scale(1.08) translateY(4px)",
                transform_origin="center",
                filter="drop-shadow(0 16px 18px rgba(22,53,76,0.12))",
                pointer_events="none",
            ),
            width="260px",
            height="245px",
            position="relative",
            display="flex",
            align_items="center",
            justify_content="center",
            overflow="visible",
        ),
        flex="0 0 280px",
        min_width="230px",
    )

def dashboard() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.flex(
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
                        line_height="1.05",
                    ),
                    rx.text(
                        (
                            "Explore your consumption and discover practical "
                            "opportunities to reduce your bill."
                        ),
                        color=MUTED,
                        font_size="1.1rem",
                        line_height="1.75",
                        max_width="760px",
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
                    flex="1 1 620px",
                    min_width="0",
                ),

                dashboard_hero_mascot(),

                align="center",
                justify="between",
                gap="2.5rem",
                flex_wrap="wrap",
                **PAGE_CONTAINER,
            ),
            padding="3.8rem 0 2.8rem",
            background=BACKGROUND,
            overflow="hidden",
        ),

        rx.box(
            rx.vstack(
                rx.text(
                    "Dashboard settings",
                    color=PRIMARY,
                    font_weight="700",
                    font_size="1.05rem",
                ),

                rx.flex(
                    rx.vstack(
                        rx.text("Household ID", color=PRIMARY),
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
                    rx.vstack(
                        rx.text("Start date", color=PRIMARY),
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
                    rx.vstack(
                        rx.text("End date", color=PRIMARY),
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
                    rx.vstack(
                        rx.text("Action", visibility="hidden"),
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
                    DashboardState.partial_data_message != "",
                    rx.callout(
                        DashboardState.partial_data_message,
                        color_scheme="orange",
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
                        hourly_chart(DashboardState.hourly_chart_data),

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