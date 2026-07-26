import reflex as rx

from ..components.navbar import navbar
from ..styles import (
    ACCENT,
    ACCENT_DARK,
    BACKGROUND,
    BORDER,
    MUTED,
    PAGE_CONTAINER,
    PRIMARY,
    SOFT_GREEN,
    SURFACE,
    TEXT,
)


def feature_card(
    icon: str,
    title: str,
    description: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.center(
                rx.text(
                    icon,
                    font_weight="700",
                    color=ACCENT,
                ),
                width="48px",
                height="48px",
                border_radius="14px",
                background=SOFT_GREEN,
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


def home() -> rx.Component:
    return rx.box(
        navbar(),

        # Hero
        rx.box(
            rx.flex(
                rx.vstack(
                    rx.text(
                        "SMART ENERGY, MADE SIMPLE",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="700",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "Use energy when it costs less.",
                        size="9",
                        color=PRIMARY,
                        line_height="1.05",
                        letter_spacing="-0.045em",
                        max_width="680px",
                    ),
                    rx.text(
                        (
                            "Volti turns your smart meter data into clear, "
                            "personalised actions that help reduce your bill "
                            "and carbon footprint."
                        ),
                        color=MUTED,
                        font_size="1.15rem",
                        line_height="1.75",
                        max_width="610px",
                    ),
                    rx.flex(
                        rx.link(
                            rx.button(
                                "Open your dashboard",
                                size="3",
                                background=ACCENT,
                                color="white",
                                border_radius="12px",
                                padding="1.4rem 1.7rem",
                                _hover={
                                    "background": ACCENT_DARK,
                                },
                            ),
                            href="/dashboard",
                        ),
                        rx.link(
                            rx.button(
                                "See how it works",
                                size="3",
                                variant="outline",
                                color=PRIMARY,
                                border_color=BORDER,
                                border_radius="12px",
                                padding="1.4rem 1.7rem",
                            ),
                            href="/how-it-works",
                        ),
                        spacing="4",
                        flex_wrap="wrap",
                    ),
                    align="start",
                    spacing="6",
                    flex="1 1 520px",
                ),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "BEST ACTION TODAY",
                            color=ACCENT,
                            font_size="0.75rem",
                            font_weight="700",
                            letter_spacing="0.1em",
                        ),
                        rx.heading(
                            "Run the dishwasher after 22:30",
                            size="6",
                            color=PRIMARY,
                            line_height="1.3",
                        ),
                        rx.text(
                            "Estimated saving",
                            color=MUTED,
                        ),
                        rx.heading(
                            "£1.20",
                            size="8",
                            color=ACCENT,
                        ),
                        rx.text(
                            "Lower cost · Lower carbon",
                            color=MUTED,
                        ),
                        align="start",
                        spacing="4",
                    ),
                    flex="1 1 340px",
                    max_width="420px",
                    padding="2.5rem",
                    background=SURFACE,
                    border=f"1px solid {BORDER}",
                    border_radius="24px",
                    box_shadow="0 22px 55px rgba(22, 53, 76, 0.12)",
                ),
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding="6rem 2rem",
                gap="4rem",
                align="center",
                justify="between",
                flex_wrap="wrap",
            ),
            background=BACKGROUND,
        ),

        # Features
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "WHY VOLTI?",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="700",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "Energy insights you can actually use",
                        size="8",
                        color=PRIMARY,
                        letter_spacing="-0.035em",
                    ),
                    rx.text(
                        (
                            "No complicated charts. No extra hardware. "
                            "Just clear recommendations based on your usage."
                        ),
                        color=MUTED,
                        font_size="1.05rem",
                    ),
                    align="center",
                    text_align="center",
                    spacing="4",
                ),
                rx.flex(
                    feature_card(
                        "£",
                        "Save money",
                        "Find cheaper times to run flexible appliances.",
                    ),
                    feature_card(
                        "⚡",
                        "Take one clear action",
                        (
                            "See what to change, when to change it "
                            "and how much you could save."
                        ),
                    ),
                    feature_card(
                        "CO₂",
                        "Use greener energy",
                        (
                            "Shift consumption towards cleaner, "
                            "lower-demand periods."
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
            background="#FFFFFF",
        ),
        width="100%",
        background=BACKGROUND,
        color=TEXT,
        min_height="100vh",
    )