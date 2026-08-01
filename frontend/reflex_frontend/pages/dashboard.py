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


def tour_chart_wrapper(
    content: rx.Component,
    *,
    chart_id: str,
    step: int,
) -> rx.Component:
    """Wrap a chart so the guide can spotlight it."""
    is_focused = (
        DashboardState.tour_open
        & (DashboardState.tour_step == step)
    )

    return rx.box(
        content,
        id=chart_id,
        class_name="volti-tour-chart",
        width="100%",
        min_width="0",
        align_self="stretch",
        position="relative",
        z_index=rx.cond(is_focused, "2302", "1"),
        border_radius="22px",
        box_shadow=rx.cond(
            is_focused,
            (
                "0 0 0 6px rgba(255,255,255,0.98), "
                "0 28px 80px rgba(0,0,0,0.38)"
            ),
            "none",
        ),
        transform=rx.cond(
            is_focused,
            "scale(1.008)",
            "scale(1)",
        ),
        transition=(
            "box-shadow 0.28s ease, "
            "transform 0.28s ease"
        ),
        scroll_margin_top="110px",
    )


def chart_tour_scroll_effect() -> rx.Component:
    """Scroll the active guide step into view."""
    return rx.cond(
        DashboardState.tour_step == 0,
        rx.script(
            """
            setTimeout(() => {
              document.getElementById('consumption-history-chart')
                ?.scrollIntoView({behavior: 'smooth', block: 'center'});
            }, 120);
            """
        ),
        rx.cond(
            DashboardState.tour_step == 1,
            rx.script(
                """
                setTimeout(() => {
                  document.getElementById('forecast-chart')
                    ?.scrollIntoView({behavior: 'smooth', block: 'center'});
                }, 120);
                """
            ),
            rx.script(
                """
                setTimeout(() => {
                  document.getElementById('hourly-breakdown-chart')
                    ?.scrollIntoView({behavior: 'smooth', block: 'center'});
                }, 120);
                """
            ),
        ),
    )


def chart_tour_overlay() -> rx.Component:
    """Render the mascot-led chart walkthrough."""
    return rx.fragment(
        chart_tour_scroll_effect(),

        rx.box(
            class_name="volti-tour-overlay",
            position="fixed",
            inset="0",
            background="rgba(7, 20, 29, 0.74)",
            backdrop_filter="blur(2px)",
            z_index="2300",
        ),

        rx.box(
            rx.flex(
                # Left mascot
                rx.center(
                    rx.image(
                        src="/mascots/thinking.png",
                        width="105px",
                        height="105px",
                        object_fit="contain",
                        filter=(
                            "drop-shadow(0 12px 18px "
                            "rgba(22,53,76,0.18))"
                        ),
                        pointer_events="none",
                    ),
                    width="125px",
                    min_width="125px",
                    background=(
                        "linear-gradient(145deg, "
                        "rgba(233,247,243,0.98), "
                        "rgba(255,255,255,0.98))"
                    ),
                    border_radius="18px",
                ),

                # Right content
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            DashboardState.tour_step_label,
                            color=ACCENT,
                            font_size="0.72rem",
                            font_weight="800",
                            letter_spacing="0.12em",
                        ),
                        rx.button(
                            "×",
                            on_click=DashboardState.close_chart_tour,
                            background="transparent",
                            color=MUTED,
                            font_size="1.25rem",
                            min_width="auto",
                            padding="0.1rem 0.35rem",
                            cursor="pointer",
                            _hover={"color": PRIMARY},
                        ),
                        width="100%",
                        justify="between",
                        align="center",
                    ),

                    rx.heading(
                        DashboardState.tour_title,
                        size="5",
                        color=PRIMARY,
                        line_height="1.2",
                    ),

                    rx.text(
                        DashboardState.tour_description,
                        color=MUTED,
                        font_size="0.86rem",
                        line_height="1.5",
                    ),

                    rx.box(
                        rx.hstack(
                            rx.text(
                                "TIP",
                                color=ACCENT,
                                font_size="0.68rem",
                                font_weight="800",
                                letter_spacing="0.1em",
                            ),
                            rx.text(
                                DashboardState.tour_tip,
                                color=PRIMARY,
                                font_size="0.8rem",
                                line_height="1.4",
                            ),
                            spacing="3",
                            align="start",
                        ),
                        width="100%",
                        padding="0.65rem 0.75rem",
                        background=SOFT_GREEN,
                        border=f"1px solid {BORDER}",
                        border_radius="11px",
                    ),

                    rx.hstack(
                        rx.button(
                            "Skip tour",
                            on_click=DashboardState.close_chart_tour,
                            background="transparent",
                            color=MUTED,
                            border=f"1px solid {BORDER}",
                            border_radius="9px",
                            cursor="pointer",
                        ),
                        rx.hstack(
                            rx.button(
                                "Back",
                                on_click=(
                                    DashboardState.previous_chart_tour_step
                                ),
                                disabled=DashboardState.tour_step == 0,
                                background="transparent",
                                color=PRIMARY,
                                border=f"1px solid {BORDER}",
                                border_radius="9px",
                                cursor="pointer",
                            ),
                            rx.button(
                                DashboardState.tour_next_label,
                                on_click=DashboardState.next_chart_tour_step,
                                background=ACCENT,
                                color="white",
                                border_radius="9px",
                                padding="0.55rem 1rem",
                                cursor="pointer",
                                _hover={"opacity": "0.92"},
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        justify="between",
                        align="center",
                    ),

                    width="100%",
                    flex="1",
                    min_width="0",
                    align="start",
                    spacing="3",
                ),

                width="100%",
                align="stretch",
                gap="0.9rem",
                flex_wrap="nowrap",
            ),
            class_name="volti-tour-panel",
            position="fixed",
            right="18px",
            bottom="18px",
            width="590px",
            max_width="calc(100vw - 28px)",
            padding="0.85rem",
            background="rgba(255,255,255,0.98)",
            border=f"1px solid {BORDER}",
            border_radius="20px",
            box_shadow="0 22px 65px rgba(0,0,0,0.26)",
            z_index="2304",
        ),
    )

def device_icon_path(device):
    """Return the matching SVG asset for a recommendation device."""
    return rx.match(
        device,

        ("Washing Machine", "/icons/washing-machine.svg"),
        ("washing machine", "/icons/washing-machine.svg"),
        ("washing_machine", "/icons/washing-machine.svg"),

        ("Dishwasher", "/icons/dishwasher.svg"),
        ("dishwasher", "/icons/dishwasher.svg"),

        ("Tumble Dryer", "/icons/tumble-dryer.svg"),
        ("tumble dryer", "/icons/tumble-dryer.svg"),
        ("tumble_dryer", "/icons/tumble-dryer.svg"),

        ("Electric Vehicle Charger", "/icons/ev-charger.svg"),
        ("Electric vehicle charger", "/icons/ev-charger.svg"),
        ("electric vehicle charger", "/icons/ev-charger.svg"),
        ("electric_vehicle_charger", "/icons/ev-charger.svg"),
        ("EV Charger", "/icons/ev-charger.svg"),
        ("EV charger", "/icons/ev-charger.svg"),
        ("ev_charger", "/icons/ev-charger.svg"),

        "/icons/default-energy.svg",
    )

def device_illustration(icon_path) -> rx.Component:
    """Render a consistent branded illustration tile."""
    return rx.center(
        rx.image(
            src=icon_path,
            width="108px",
            height="108px",
            object_fit="contain",
        ),
        width="100%",
        min_height="142px",
        padding="0.9rem",
        background=(
            "linear-gradient(145deg, "
            "rgba(233,247,243,0.96), "
            "rgba(252,253,251,0.94))"
        ),
        border=f"1px solid {BORDER}",
        border_radius="16px",
        overflow="hidden",
    )


def recommendation_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            device_illustration(
                device_icon_path(item["device"])
            ),
            rx.vstack(
                rx.heading(
                    item["device"],
                    size="5",
                    color=PRIMARY,
                    line_height="1.25",
                ),
                rx.hstack(
                    rx.text(
                        "Recommended time",
                        color=MUTED,
                        font_size="0.78rem",
                    ),
                    rx.text(
                        item["time_shift"],
                        color=PRIMARY,
                        font_weight="700",
                        font_size="0.9rem",
                    ),
                    width="100%",
                    justify="between",
                    align="center",
                    gap="0.75rem",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Estimated saving",
                            color=MUTED,
                            font_size="0.75rem",
                        ),
                        rx.heading(
                            item["saving"],
                            size="6",
                            color=ACCENT,
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text(
                            "Carbon reduction",
                            color=MUTED,
                            font_size="0.75rem",
                        ),
                        rx.text(
                            item["carbon"],
                            color=PRIMARY,
                            font_weight="700",
                            font_size="0.9rem",
                        ),
                        align="end",
                        spacing="1",
                    ),
                    width="100%",
                    justify="between",
                    align="end",
                ),
                width="100%",
                align="start",
                spacing="4",
                padding="0.25rem 0.15rem 0.1rem",
            ),
            width="100%",
            height="100%",
            align="stretch",
            spacing="4",
        ),
        flex="1 1 245px",
        min_width="0",
        padding="1rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="20px",
        box_shadow="0 12px 30px rgba(22,53,76,0.06)",
        transition="transform 0.2s ease, box-shadow 0.2s ease",
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 18px 40px rgba(22,53,76,0.10)",
        },
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
                        rx.select(
                            DashboardState.household_ids,
                            value=DashboardState.household_id,
                            on_change=DashboardState.update_household_id,
                            placeholder="Select a household",
                            disabled=~DashboardState.households_loaded,
                            width="100%",
                            size="3",
                            variant="surface",
                            radius="large",
                            color_scheme="teal",
                            position="popper",
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
                    rx.vstack(
                        rx.callout(
                            "Energy data loaded successfully.",
                            color_scheme="green",
                            width="100%",
                        ),
                        rx.cond(
                            DashboardState.household_tariff == "Std",
                            rx.callout(
                                (
                                    "This household uses a standard fixed-price tariff. "
                                    "Electricity prices remain the same throughout the day, "
                                    "so shifting appliance use to another hour does not "
                                    "create a cost saving."
                                ),
                                color_scheme="blue",
                                width="100%",
                            ),
                            rx.cond(
                                DashboardState.household_tariff == "ToU",
                                rx.callout(
                                    (
                                        "This household uses a Time-of-Use tariff. "
                                        "Electricity prices vary depending on the time of day, "
                                        "so Volti can identify lower-cost periods for "
                                        "appliance use."
                                    ),
                                    color_scheme="teal",
                                    width="100%",
                                ),
                                rx.callout(
                                    "Tariff information is unavailable for this household.",
                                    color_scheme="gray",
                                    width="100%",
                                ),
                            ),
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.fragment(),
                ),

                rx.cond(
                    DashboardState.dashboard_loaded,
                    rx.vstack(
                        rx.hstack(
                            rx.button(
                                rx.hstack(
                                    rx.text("ⓘ", font_size="1rem"),
                                    rx.text(
                                        "How to read these charts",
                                        font_weight="700",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                on_click=DashboardState.start_chart_tour,
                                background=SOFT_GREEN,
                                color=PRIMARY,
                                border=f"1px solid {BORDER}",
                                border_radius="11px",
                                cursor="pointer",
                                _hover={
                                    "border_color": ACCENT,
                                    "color": ACCENT,
                                },
                            ),
                            width="100%",
                            justify="end",
                        ),

                        tour_chart_wrapper(
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
                            chart_id="consumption-history-chart",
                            step=0,
                        ),

                        tour_chart_wrapper(
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
                            chart_id="forecast-chart",
                            step=1,
                        ),

                        tour_chart_wrapper(
                            hourly_chart(
                                DashboardState.hourly_chart_data
                            ),
                            chart_id="hourly-breakdown-chart",
                            step=2,
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
                                            header=rx.box(
                                                rx.hstack(
                                                    rx.vstack(
                                                        rx.text(
                                                            DashboardState.anomaly_count_text,
                                                            color=PRIMARY,
                                                            font_weight="700",
                                                            font_size="1rem",
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
                                                width="100%",
                                                padding="1.1rem 1.25rem",
                                                background=SURFACE,
                                            ),
                                            content=rx.box(
                                                rx.vstack(
                                                    rx.callout(
                                                        DashboardState.anomaly_summary,
                                                        color_scheme="red",
                                                        variant="soft",
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
                                                ),
                                                width="100%",
                                                padding="1.25rem",
                                                background="#FFFDFC",
                                                border_top=f"1px solid {BORDER}",
                                            ),
                                            background=SURFACE,
                                        ),
                                        type="single",
                                        collapsible=True,
                                        width="100%",
                                        background=SURFACE,
                                        border=f"1px solid {BORDER}",
                                        border_radius="16px",
                                        overflow="hidden",
                                        box_shadow="0 8px 24px rgba(22,53,76,0.05)",
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
                # Best action card
                rx.box(
                    rx.flex(
                        # Text section
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
                                    line_height="1.25",
                                ),
                                rx.heading(
                                    (
                                        "Load a household to receive "
                                        "personalised advice"
                                    ),
                                    size="6",
                                    color=PRIMARY,
                                    line_height="1.25",
                                ),
                            ),

                            rx.cond(
                                DashboardState.dashboard_loaded,
                                rx.text(
                                    DashboardState.best_action_message,
                                    color=MUTED,
                                    font_size="1rem",
                                    line_height="1.7",
                                ),
                                rx.text(
                                    (
                                        "Volti will identify your clearest saving "
                                        "opportunity and display it here."
                                    ),
                                    color=MUTED,
                                    font_size="1rem",
                                    line_height="1.7",
                                ),
                            ),

                            align="start",
                            spacing="4",
                            flex="1",
                        ),

                        # Device illustration
                        rx.cond(
                            DashboardState.dashboard_loaded,
                            rx.center(
                                rx.image(
                                    src=device_icon_path(
                                        DashboardState.best_action_device
                                    ),
                                    width="112px",
                                    height="112px",
                                    object_fit="contain",
                                    alt="Recommended device",
                                ),
                                width="150px",
                                height="150px",
                                min_width="150px",
                                background="rgba(255, 255, 255, 0.58)",
                                border=f"1px solid {BORDER}",
                                border_radius="20px",
                            ),
                            rx.fragment(),
                        ),

                        width="100%",
                        align="center",
                        justify="between",
                        gap="2rem",
                        flex_wrap="wrap",
                    ),
                    width="100%",
                    padding="2rem",
                    background=SOFT_GREEN,
                    border=f"1px solid {BORDER}",
                    border_radius="20px",
                ),

                # Metric cards
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

        rx.cond(
            DashboardState.tour_open,
            chart_tour_overlay(),
            rx.fragment(),
        ),

        floating_coach(),

        min_height="100vh",
        background=BACKGROUND,
    )