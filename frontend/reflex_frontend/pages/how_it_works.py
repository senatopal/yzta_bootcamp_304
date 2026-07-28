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


def process_step(
    step_number: str,
    eyebrow: str,
    title: str,
    description: str,
    image_src: str,
    details: list[str],
    image_left: bool = True,
) -> rx.Component:
    """Render a wide alternating process section."""

    image_panel = rx.center(
        rx.image(
            src=image_src,
            width="86%",
            max_width="430px",
            height="auto",
            object_fit="contain",
        ),
        flex="1 1 430px",
        min_height="410px",
        padding="2rem",
        background=(
            "linear-gradient(145deg, "
            "rgba(233,247,243,0.96), "
            "rgba(255,255,255,0.96))"
        ),
        border=f"1px solid {BORDER}",
        border_radius="28px",
    )

    text_panel = rx.vstack(
        rx.box(
            rx.text(
                step_number,
                color="white",
                font_size="0.76rem",
                font_weight="800",
                letter_spacing="0.12em",
            ),
            padding="0.5rem 0.85rem",
            background=ACCENT,
            border_radius="999px",
        ),
        rx.text(
            eyebrow,
            color=ACCENT,
            font_size="0.78rem",
            font_weight="800",
            letter_spacing="0.14em",
        ),
        rx.heading(
            title,
            size="8",
            color=PRIMARY,
            letter_spacing="-0.035em",
            line_height="1.12",
        ),
        rx.text(
            description,
            color=MUTED,
            font_size="1.05rem",
            line_height="1.8",
            max_width="580px",
        ),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(
                        width="9px",
                        height="9px",
                        border_radius="50%",
                        background=ACCENT,
                        flex_shrink="0",
                        margin_top="0.5rem",
                    ),
                    rx.text(
                        detail,
                        color=PRIMARY,
                        font_size="0.96rem",
                        line_height="1.65",
                    ),
                    width="100%",
                    align="start",
                    spacing="3",
                )
                for detail in details
            ],
            width="100%",
            align="start",
            spacing="3",
            margin_top="0.5rem",
        ),
        flex="1 1 430px",
        align="start",
        justify="center",
        spacing="4",
        padding="2rem",
    )

    children = (
        [image_panel, text_panel]
        if image_left
        else [text_panel, image_panel]
    )

    return rx.box(
        rx.flex(
            *children,
            width="100%",
            align="stretch",
            gap="3rem",
            flex_wrap="wrap",
        ),
        width="100%",
        padding="1.5rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="32px",
        box_shadow="0 18px 46px rgba(22, 53, 76, 0.07)",
    )


def action_result_section() -> rx.Component:
    """Render Step 03 with the recommendation mascot illustration."""

    text_panel = rx.vstack(
        rx.box(
            rx.text(
                "STEP 03",
                color="white",
                font_size="0.76rem",
                font_weight="800",
                letter_spacing="0.12em",
            ),
            padding="0.5rem 0.85rem",
            background=ACCENT,
            border_radius="999px",
        ),
        rx.text(
            "ACT",
            color=ACCENT,
            font_size="0.78rem",
            font_weight="800",
            letter_spacing="0.14em",
        ),
        rx.heading(
            "Receive one clear action",
            size="8",
            color=PRIMARY,
            letter_spacing="-0.035em",
            line_height="1.12",
        ),
        rx.text(
            (
                "Volti converts complex energy analysis into one "
                "practical recommendation that explains what to "
                "change, when to change it and why it matters."
            ),
            color=MUTED,
            font_size="1.05rem",
            line_height="1.8",
            max_width="590px",
        ),
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="9px",
                    height="9px",
                    border_radius="50%",
                    background=ACCENT,
                    flex_shrink="0",
                    margin_top="0.5rem",
                ),
                rx.text(
                    "See the best time to run a flexible appliance.",
                    color=PRIMARY,
                    line_height="1.65",
                ),
                align="start",
                spacing="3",
            ),
            rx.hstack(
                rx.box(
                    width="9px",
                    height="9px",
                    border_radius="50%",
                    background=ACCENT,
                    flex_shrink="0",
                    margin_top="0.5rem",
                ),
                rx.text(
                    "Understand the estimated cost and carbon benefit.",
                    color=PRIMARY,
                    line_height="1.65",
                ),
                align="start",
                spacing="3",
            ),
            align="start",
            spacing="3",
        ),
        flex="1 1 430px",
        align="start",
        justify="center",
        spacing="4",
        padding="2rem",
    )

    illustration_panel = rx.center(
        rx.box(
            rx.box(
                position="absolute",
                inset="9% 7% 7%",
                background=(
                    "radial-gradient(circle at 50% 42%, "
                    "rgba(255,255,255,0.98) 0%, "
                    "rgba(236,247,243,0.88) 58%, "
                    "rgba(236,247,243,0.30) 100%)"
                ),
                border="1px solid rgba(22,135,126,0.10)",
                border_radius="34px",
                z_index="0",
            ),
            rx.image(
                src="/illustrations/step3-mascot.png",
                width="100%",
                max_width="340px",
                height="auto",
                object_fit="contain",
                position="relative",
                z_index="2",
                filter="drop-shadow(0 20px 28px rgba(22,53,76,0.14))",
                pointer_events="none",
            ),
            width="100%",
            min_height="360px",
            position="relative",
            display="flex",
            align_items="center",
            justify_content="center",
            overflow="visible",
        ),
        flex="1 1 380px",
        min_height="360px",
        padding="1.2rem",
        background=(
            "linear-gradient(145deg, "
            "rgba(255,255,255,0.72), "
            "rgba(233,247,243,0.72))"
        ),
        border="1px solid rgba(22,135,126,0.12)",
        border_radius="28px",
        overflow="hidden",
    )

    return rx.box(
        rx.flex(
            text_panel,
            illustration_panel,
            width="100%",
            align="stretch",
            gap="2.25rem",
            flex_wrap="wrap",
        ),
        width="100%",
        padding="1.5rem",
        background=SOFT_GREEN,
        border=f"1px solid {BORDER}",
        border_radius="32px",
        box_shadow="0 18px 46px rgba(22,53,76,0.07)",
    )


def how_it_works() -> rx.Component:
    return rx.box(
        navbar(),

        # Hero
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

        # Process
        rx.box(
            rx.vstack(
                process_step(
                    step_number="STEP 01",
                    eyebrow="CONNECT",
                    title="Connect your energy data",
                    description=(
                        "Volti uses half-hourly smart meter data to "
                        "understand when and how much electricity "
                        "your home consumes."
                    ),
                    image_src="/illustrations/step-connect-data.svg",
                    details=[
                        "Reads household consumption at half-hour intervals.",
                        "Connects usage with tariff and pricing information.",
                        "Keeps the original energy data structured and traceable.",
                    ],
                    image_left=True,
                ),

                process_step(
                    step_number="STEP 02",
                    eyebrow="ANALYSE",
                    title="Analyse usage, prices and patterns",
                    description=(
                        "Consumption, tariff and forecast information are "
                        "compared to identify costly periods, unusual "
                        "activity and flexible loads."
                    ),
                    image_src="/illustrations/step-analyse.svg",
                    details=[
                        "Compares consumption with changing electricity prices.",
                        "Forecasts expected demand for the next 24 hours.",
                        "Detects unusual usage and potential energy waste.",
                    ],
                    image_left=False,
                ),

                action_result_section(),

                spacing="7",
                **PAGE_CONTAINER,
            ),
            padding="5rem 0 6rem",
            background=SURFACE,
        ),

        # No extra hardware
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
