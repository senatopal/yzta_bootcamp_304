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


def principle_card(
    icon: str,
    title: str,
    description: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.center(
                rx.text(
                    icon,
                    color=ACCENT,
                    font_weight="700",
                ),
                width="48px",
                height="48px",
                background=SOFT_GREEN,
                border_radius="14px",
            ),
            rx.heading(
                title,
                size="5",
                color=PRIMARY,
            ),
            rx.text(
                description,
                color=MUTED,
                line_height="1.7",
            ),
            align="start",
            spacing="4",
        ),
        flex="1 1 260px",
        padding="2rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="20px",
        box_shadow="0 12px 30px rgba(22, 53, 76, 0.06)",
    )


def about() -> rx.Component:
    return rx.box(
        navbar(),

        rx.box(
            rx.vstack(
                rx.text(
                    "ABOUT VOLTI",
                    color=ACCENT,
                    font_size="0.8rem",
                    font_weight="700",
                    letter_spacing="0.12em",
                ),
                rx.heading(
                    "Making smarter energy choices easier",
                    size="9",
                    color=PRIMARY,
                    max_width="850px",
                    text_align="center",
                    line_height="1.08",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    (
                        "Volti helps households understand their electricity "
                        "use and take simple, practical steps towards lower "
                        "bills and a smaller carbon footprint."
                    ),
                    color=MUTED,
                    font_size="1.15rem",
                    max_width="750px",
                    text_align="center",
                    line_height="1.75",
                ),
                align="center",
                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="6rem 0",
            background=BACKGROUND,
        ),

        rx.box(
            rx.flex(
                rx.box(
                    rx.vstack(
                        rx.text(
                            "OUR MISSION",
                            color="#9FE0D8",
                            font_size="0.8rem",
                            font_weight="700",
                            letter_spacing="0.12em",
                        ),
                        rx.heading(
                            "Turn energy data into useful action",
                            size="7",
                            color="white",
                        ),
                        rx.text(
                            (
                                "Smart meters generate valuable information, "
                                "but consumption charts rarely explain what "
                                "someone should do next. Volti bridges that gap."
                            ),
                            color="#E2ECEF",
                            line_height="1.75",
                        ),
                        align="start",
                        spacing="5",
                    ),
                    flex="1 1 480px",
                    padding="2.5rem",
                    background=PRIMARY,
                    border_radius="24px",
                ),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "WHO IT IS FOR",
                            color=ACCENT,
                            font_size="0.8rem",
                            font_weight="700",
                            letter_spacing="0.12em",
                        ),
                        rx.heading(
                            "Built for real households",
                            size="7",
                            color=PRIMARY,
                        ),
                        rx.text(
                            (
                                "Volti is designed for busy households that "
                                "want to reduce energy costs without spending "
                                "hours analysing tariffs or technical data."
                            ),
                            color=MUTED,
                            line_height="1.75",
                        ),
                        align="start",
                        spacing="5",
                    ),
                    flex="1 1 380px",
                    padding="2.5rem",
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="24px",
                ),
                gap="1.5rem",
                flex_wrap="wrap",
                **PAGE_CONTAINER,
            ),
            padding="5rem 0",
            background=SURFACE,
        ),

        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "OUR PRINCIPLES",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="700",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "Simple, transparent and action-focused",
                        size="8",
                        color=PRIMARY,
                    ),
                    align="center",
                    text_align="center",
                    spacing="4",
                ),
                rx.flex(
                    principle_card(
                        "✓",
                        "Clarity first",
                        (
                            "The most important recommendation is shown "
                            "first and written in clear language."
                        ),
                    ),
                    principle_card(
                        "🔒",
                        "Privacy conscious",
                        (
                            "Energy information should be handled "
                            "transparently and used only for relevant insights."
                        ),
                    ),
                    principle_card(
                        "CO₂",
                        "Cost and carbon",
                        (
                            "Financial and environmental impact are shown "
                            "together to support balanced decisions."
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
            background=BACKGROUND,
        ),

        min_height="100vh",
        background=BACKGROUND,
    )