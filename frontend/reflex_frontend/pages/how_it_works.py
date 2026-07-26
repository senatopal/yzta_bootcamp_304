import reflex as rx

from reflex_frontend.components.navbar import navbar
from reflex_frontend.styles import (
    ACCENT,
    BACKGROUND,
    BORDER,
    MUTED,
    PAGE_CONTAINER,
    PRIMARY,
    SOFT_GREEN,
    SURFACE,
)


def process_card(
    number: str,
    icon: str,
    title: str,
    description: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.text(
                        icon,
                        font_size="1.35rem",
                    ),
                    width="52px",
                    height="52px",
                    background=SOFT_GREEN,
                    border_radius="15px",
                ),
                rx.text(
                    number,
                    color=ACCENT,
                    font_size="0.8rem",
                    font_weight="700",
                    letter_spacing="0.1em",
                ),
                justify="between",
                width="100%",
                align="center",
            ),
            rx.heading(
                title,
                size="6",
                color=PRIMARY,
                line_height="1.25",
            ),
            rx.text(
                description,
                color=MUTED,
                line_height="1.75",
            ),
            align="start",
            spacing="5",
        ),
        flex="1 1 280px",
        padding="2rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="20px",
        box_shadow="0 12px 30px rgba(22, 53, 76, 0.06)",
    )


def how_it_works() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.vstack(
                rx.text(
                    "HOW VOLTI WORKS",
                    color=ACCENT,
                    font_size="0.8rem",
                    font_weight="700",
                    letter_spacing="0.12em",
                ),
                rx.heading(
                    "From smart meter data to one clear action",
                    size="9",
                    color=PRIMARY,
                    max_width="820px",
                    text_align="center",
                    line_height="1.08",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    (
                        "Volti analyses your energy use and turns complex "
                        "consumption patterns into practical recommendations."
                    ),
                    color=MUTED,
                    font_size="1.15rem",
                    max_width="700px",
                    text_align="center",
                    line_height="1.75",
                ),
                align="center",
                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="6rem 0 5rem",
            background=BACKGROUND,
        ),

        rx.box(
            rx.vstack(
                rx.flex(
                    process_card(
                        "STEP 01",
                        "📊",
                        "Connect your energy data",
                        (
                            "Volti uses half-hourly smart meter data to "
                            "understand when and how much electricity "
                            "your home consumes."
                        ),
                    ),
                    process_card(
                        "STEP 02",
                        "⚙️",
                        "Analyse usage and prices",
                        (
                            "Consumption, tariff and forecast information "
                            "are compared to identify expensive periods "
                            "and unusual activity."
                        ),
                    ),
                    process_card(
                        "STEP 03",
                        "⚡",
                        "Receive one clear action",
                        (
                            "Volti explains what to change, when to change "
                            "it and how much money and carbon you could save."
                        ),
                    ),
                    width="100%",
                    gap="1.5rem",
                    flex_wrap="wrap",
                ),
                spacing="8",
                **PAGE_CONTAINER,
            ),
            padding="5rem 0",
            background=SURFACE,
        ),

        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text(
                        "NO EXTRA HARDWARE",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="700",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "Designed for everyday households",
                        size="8",
                        color=PRIMARY,
                        letter_spacing="-0.03em",
                    ),
                    rx.text(
                        (
                            "You do not need an electric vehicle, battery "
                            "or additional monitoring equipment to receive "
                            "useful energy insights."
                        ),
                        color=MUTED,
                        font_size="1.05rem",
                        line_height="1.75",
                    ),
                    align="start",
                    spacing="4",
                    flex="1 1 420px",
                ),
                rx.vstack(
                    rx.text("✓ Personalised consumption overview"),
                    rx.text("✓ Peak and lower-cost period identification"),
                    rx.text("✓ Appliance scheduling recommendations"),
                    rx.text("✓ Cost and carbon impact together"),
                    color=PRIMARY,
                    font_weight="600",
                    line_height="1.8",
                    align="start",
                    spacing="4",
                    flex="1 1 360px",
                    padding="2rem",
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="20px",
                ),
                gap="3rem",
                align="center",
                flex_wrap="wrap",
                **PAGE_CONTAINER,
            ),
            padding="5rem 0",
            background=SOFT_GREEN,
        ),

        min_height="100vh",
        background=BACKGROUND,
    )