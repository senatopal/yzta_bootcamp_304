import reflex as rx

from ..styles import (
    ACCENT,
    BORDER,
    PAGE_WIDTH,
    PRIMARY,
    SURFACE,
    TEXT,
)


def nav_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        color=TEXT,
        font_weight="600",
        text_decoration="none",
        padding="0.55rem 0.8rem",
        border_radius="10px",
        _hover={
            "color": ACCENT,
            "background": "#EAF7F4",
        },
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.box(
                        width="12px",
                        height="12px",
                        border_radius="50%",
                        background=ACCENT,
                    ),
                    rx.heading(
                        "Volti",
                        size="6",
                        color=PRIMARY,
                        letter_spacing="-0.03em",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            rx.hstack(
                nav_link("Home", "/"),
                nav_link("Dashboard", "/dashboard"),
                nav_link("How It Works", "/how-it-works"),
                nav_link("About", "/about"),
                spacing="2",
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width=PAGE_WIDTH,
            margin="0 auto",
            padding="1rem 2rem",
        ),
        position="sticky",
        top="0",
        z_index="1000",
        width="100%",
        background=SURFACE,
        border_bottom=f"1px solid {BORDER}",
        box_shadow="0 4px 18px rgba(22, 53, 76, 0.05)",
    )