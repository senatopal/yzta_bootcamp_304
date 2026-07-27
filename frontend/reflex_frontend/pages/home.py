import reflex as rx

from ..components.navbar import navbar
from ..styles import (
    ACCENT,
    BACKGROUND,
    BORDER,
    MUTED,
    PAGE_CONTAINER,
    PRIMARY,
    SOFT_GREEN,
    SURFACE,
    TEXT,
)

HERO_BACKGROUND = "/backgrounds/hero-bg-mesh-blobs.svg"

# Alternative:
# HERO_BACKGROUND = "/backgrounds/hero-bg-timeofuse-wave.svg"


def feature_card(
    image_src: str,
    eyebrow: str,
    title: str,
    description: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            # Illustration area
            rx.center(
                rx.image(
                    src=image_src,
                    width="74%",
                    max_width="220px",
                    height="auto",
                    object_fit="contain",
                ),
                width="100%",
                height="250px",
                padding="1rem",
                background=(
                    "linear-gradient(145deg, "
                    "rgba(233,247,243,0.96), "
                    "rgba(255,255,255,0.94))"
                ),
                border_bottom=f"1px solid {BORDER}",
            ),

            # Text content
            rx.vstack(
                rx.text(
                    eyebrow,
                    color=ACCENT,
                    font_size="0.8rem",
                    font_weight="800",
                    letter_spacing="0.16em",
                ),
                rx.heading(
                    title,
                    size="6",
                    color=PRIMARY,
                    line_height="1.2",
                ),
                rx.text(
                    description,
                    color=MUTED,
                    line_height="1.75",
                    font_size="1rem",
                    max_width="320px",
                ),
                rx.link(
                    rx.hstack(
                        rx.text(
                            "See how it works",
                            font_weight="700",
                        ),
                        rx.text(
                            "→",
                            font_size="1.1rem",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    href="/how-it-works",
                    color=ACCENT,
                    text_decoration="none",
                    margin_top="auto",
                    _hover={
                        "color": PRIMARY,
                    },
                ),
                width="100%",
                height="100%",
                align="start",
                text_align="left",
                spacing="4",
                padding="1.75rem",
            ),

            width="100%",
            height="100%",
            align="stretch",
            spacing="0",
        ),
        flex="1 1 300px",
        min_width="0",
        min_height="520px",
        overflow="hidden",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="24px",
        box_shadow="0 16px 38px rgba(22, 53, 76, 0.07)",
        transition="transform 0.22s ease, box-shadow 0.22s ease",
        _hover={
            "transform": "translateY(-6px)",
            "box_shadow": "0 24px 52px rgba(22, 53, 76, 0.12)",
        },
    )


def home() -> rx.Component:
    return rx.box(
        navbar(),

        # Hero
        rx.box(
            # Background layer
            rx.box(
                position="absolute",
                inset="0",
                background_image=f"url('{HERO_BACKGROUND}')",
                background_size="cover",
                background_position="center",
                background_repeat="no-repeat",
                opacity="0.92",
                z_index="0",
            ),

            # Hero content
            rx.flex(
                # Left side
                rx.vstack(
                    rx.text(
                        "SMART ENERGY, MADE SIMPLE",
                        color=ACCENT,
                        font_size="0.82rem",
                        font_weight="700",
                        letter_spacing="0.16em",
                    ),
                    rx.heading(
                        "Use energy when it costs less.",
                        size="9",
                        color=PRIMARY,
                        max_width="720px",
                        letter_spacing="-0.045em",
                        line_height="1.06",
                    ),
                    rx.text(
                        (
                            "Volti turns your smart meter data into clear, "
                            "personalised actions that help reduce your bill "
                            "and carbon footprint."
                        ),
                        color=MUTED,
                        font_size="1.1rem",
                        line_height="1.8",
                        max_width="720px",
                    ),
                    rx.hstack(
                        rx.button(
                            "Open your dashboard",
                            on_click=rx.redirect("/dashboard"),
                            background=ACCENT,
                            color="white",
                            border_radius="12px",
                            padding="1.3rem 1.7rem",
                            cursor="pointer",
                            _hover={
                                "opacity": "0.92",
                            },
                        ),
                        rx.button(
                            "See how it works",
                            on_click=rx.redirect("/how-it-works"),
                            background="rgba(255,255,255,0.68)",
                            color=PRIMARY,
                            border=f"1px solid {ACCENT}",
                            border_radius="12px",
                            padding="1.3rem 1.7rem",
                            backdrop_filter="blur(8px)",
                            cursor="pointer",
                        ),
                        spacing="4",
                        flex_wrap="wrap",
                    ),
                    align="start",
                    spacing="5",
                    flex="1 1 560px",
                ),

                # Right action card
                rx.box(
                    rx.vstack(
                        rx.text(
                            "BEST ACTION TODAY",
                            color=ACCENT,
                            font_size="0.8rem",
                            font_weight="700",
                            letter_spacing="0.12em",
                        ),
                        rx.heading(
                            "Run the dishwasher after 22:30",
                            size="7",
                            color=PRIMARY,
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
                    flex="0 1 430px",
                    padding="2.5rem",
                    background="rgba(255,255,255,0.82)",
                    backdrop_filter="blur(12px)",
                    border=f"1px solid {BORDER}",
                    border_radius="26px",
                    box_shadow="0 20px 50px rgba(22,53,76,0.12)",
                ),

                align="center",
                justify="between",
                gap="4rem",
                flex_wrap="wrap",
                position="relative",
                z_index="1",
                **PAGE_CONTAINER,
            ),

            position="relative",
            overflow="hidden",
            padding="5.5rem 0",
            min_height="680px",
            display="flex",
            align_items="center",
        ),

        # Why Volti?
        rx.box(
            rx.vstack(
                # Section heading
                rx.vstack(
                    rx.box(
                        rx.text(
                            "WHY VOLTI?",
                            color=ACCENT,
                            font_size="0.9rem",
                            font_weight="800",
                            letter_spacing="0.18em",
                            text_align="center",
                        ),
                        padding="0.5rem 1rem",
                        background="rgba(22, 135, 126, 0.08)",
                        border="1px solid rgba(22, 135, 126, 0.18)",
                        border_radius="999px",
                    ),
                    rx.heading(
                        "Energy insights you can actually use",
                        size="8",
                        color=PRIMARY,
                        letter_spacing="-0.04em",
                        text_align="center",
                        width="100%",
                    ),
                    rx.text(
                        (
                            "No complicated charts. No extra hardware. "
                            "Just clear recommendations based on your usage."
                        ),
                        color=MUTED,
                        font_size="1.08rem",
                        line_height="1.75",
                        max_width="760px",
                        text_align="center",
                        width="100%",
                    ),
                    width="100%",
                    align="center",
                    justify="center",
                    spacing="5",
                ),

                # Professional illustration cards
                rx.flex(
                    feature_card(
                        "/illustrations/why-save-money.svg",
                        "LOWER COSTS",
                        "Save money",
                        (
                            "Find cheaper times to run flexible appliances "
                            "and understand where your biggest savings are."
                        ),
                    ),
                    feature_card(
                        "/illustrations/why-take-action.svg",
                        "CLEAR NEXT STEP",
                        "Take one clear action",
                        (
                            "See exactly what to change, when to change it "
                            "and how much the action could save."
                        ),
                    ),
                    feature_card(
                        "/illustrations/why-greener-energy.svg",
                        "LOWER CARBON",
                        "Use greener energy",
                        (
                            "Shift flexible consumption towards cleaner, "
                            "lower-demand periods without changing your routine."
                        ),
                    ),
                    width="100%",
                    gap="1.5rem",
                    align="stretch",
                    flex_wrap="wrap",
                ),

                spacing="8",
                **PAGE_CONTAINER,
            ),
            padding="6rem 0",
            background="#FFFFFF",
        ),

        width="100%",
        background=BACKGROUND,
        color=TEXT,
        min_height="100vh",
    )