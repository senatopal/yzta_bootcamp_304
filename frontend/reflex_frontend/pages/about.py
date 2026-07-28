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


TEAM_MEMBERS = [
    {
        "name": "Merve Günsay",
        "role": "Product Owner / Contributed to UI/UX",
        "initials": "01",
        "image_src": "/team/merve.jpg",
        "linkedin_url": "https://www.linkedin.com/in/merve-gunsay/",
        "image_position": "center 60%",
    },
    {
        "name": "Senanur Topal",
        "role": "Scrum Master / Contributed to Backend Development",
        "initials": "02",
        "image_src": "",
        "linkedin_url": "",
    },
    {
        "name": "Yasemin Koçbıyık",
        "role": "Machine Learning / Model Developer",
        "initials": "03",
        "image_src": "",
        "linkedin_url": "https://www.linkedin.com/in/yasemin-kocbiyik/",
    },
    {
        "name": "Reyyan Temel",
        "role": "Data / Backend Developer",
        "initials": "04",
        "image_src": "",
        "linkedin_url": "https://www.linkedin.com/in/reyyan-temel-845258219/",
    },
    {
        "name": "Betül İrem Yardımcı",
        "role": "Frontend Developer / AI Integration",
        "initials": "05",
        "image_src": "/team/betul-irem.jpeg",
        "linkedin_url": "https://www.linkedin.com/in/betül-irem-yardımcı-aa17a2217/",
        "image_position": "center center",
    },
]


def information_card(
    eyebrow: str,
    title: str,
    description: str,
    *,
    dark: bool = False,
    soft: bool = False,
) -> rx.Component:
    background = PRIMARY if dark else SOFT_GREEN if soft else SURFACE
    title_color = "white" if dark else PRIMARY
    body_color = "rgba(255,255,255,0.78)" if dark else MUTED
    eyebrow_color = "#9FE0D8" if dark else ACCENT
    border_color = PRIMARY if dark else BORDER

    return rx.box(
        rx.vstack(
            rx.text(
                eyebrow,
                color=eyebrow_color,
                font_size="0.8rem",
                font_weight="800",
                letter_spacing="0.14em",
            ),
            rx.heading(
                title,
                size="7",
                color=title_color,
                line_height="1.25",
            ),
            rx.text(
                description,
                color=body_color,
                line_height="1.75",
                font_size="1rem",
            ),
            align="start",
            spacing="5",
        ),
        flex="1 1 300px",
        min_width="280px",
        min_height="300px",
        padding="2.5rem",
        background=background,
        border=f"1px solid {border_color}",
        border_radius="24px",
        box_shadow=(
            "0 18px 42px rgba(22,53,76,0.10)"
            if dark
            else "0 14px 34px rgba(22,53,76,0.05)"
        ),
    )


def team_member_card(
    name: str,
    role: str,
    initials: str,
    image_src: str,
    linkedin_url: str,
    image_position: str = "center center",
) -> rx.Component:
    avatar = (
        rx.image(
            src=image_src,
            width="132px",
            height="132px",
            object_fit="cover",
            object_position=image_position,
            border_radius="50%",
            border="5px solid rgba(255,255,255,0.92)",
            box_shadow="0 12px 30px rgba(22,53,76,0.13)",
        )
        if image_src
        else rx.center(
            rx.text(
                initials,
                color=ACCENT,
                font_size="1.35rem",
                font_weight="800",
                letter_spacing="0.08em",
            ),
            width="132px",
            height="132px",
            border_radius="50%",
            background=SOFT_GREEN,
            border=f"1px solid {BORDER}",
            box_shadow="0 12px 30px rgba(22,53,76,0.08)",
        )
    )

    linkedin_component = (
        rx.link(
            rx.hstack(
                rx.image(
                    src="/icons/linkedin.svg",
                    width="18px",
                    height="18px",
                    object_fit="contain",
                    alt="LinkedIn",
                ),
                rx.text("LinkedIn", font_weight="700"),
                spacing="2",
                align="center",
                justify="center",
            ),
            href=linkedin_url,
            target="_blank",
            rel="noopener noreferrer",
            color=ACCENT,
            text_decoration="none",
            padding="0.65rem 1rem",
            border=f"1px solid {BORDER}",
            border_radius="10px",
            _hover={
                "background": SOFT_GREEN,
                "color": PRIMARY,
            },
        )
        if linkedin_url
        else rx.box(
            rx.hstack(
                rx.image(
                    src="/icons/linkedin.svg",
                    width="18px",
                    height="18px",
                    object_fit="contain",
                    alt="LinkedIn",
                    opacity="0.55",
                ),
                rx.text("LinkedIn coming soon", font_weight="700"),
                spacing="2",
                align="center",
                justify="center",
            ),
            color=MUTED,
            padding="0.65rem 1rem",
            border=f"1px solid {BORDER}",
            border_radius="10px",
            background=BACKGROUND,
        )
    )

    return rx.box(
        rx.vstack(
            avatar,
            rx.vstack(
                rx.heading(
                    name,
                    size="5",
                    color=PRIMARY,
                    text_align="center",
                ),
                rx.text(
                    role,
                    color=MUTED,
                    font_size="0.95rem",
                    line_height="1.6",
                    text_align="center",
                ),
                align="center",
                spacing="2",
            ),
            linkedin_component,
            width="100%",
            height="100%",
            align="center",
            justify="between",
            spacing="5",
        ),
        flex="0 1 calc(33.333% - 1rem)",
        min_width="260px",
        min_height="340px",
        padding="2rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="22px",
        box_shadow="0 14px 34px rgba(22,53,76,0.06)",
        transition="transform 0.22s ease, box-shadow 0.22s ease",
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 22px 44px rgba(22,53,76,0.11)",
        },
    )


def about() -> rx.Component:
    return rx.box(
        navbar(),

        # About introduction
        rx.box(
            rx.vstack(
                rx.box(
                    rx.text(
                        "ABOUT VOLTI",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="800",
                        letter_spacing="0.16em",
                    ),
                    padding="0.5rem 1rem",
                    background="rgba(22,135,126,0.08)",
                    border="1px solid rgba(22,135,126,0.18)",
                    border_radius="999px",
                ),
                rx.heading(
                    "Making household energy decisions simpler",
                    size="9",
                    color=PRIMARY,
                    max_width="850px",
                    text_align="center",
                    line_height="1.08",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    (
                        "Volti turns complex smart meter information into clear, "
                        "practical guidance that households can understand and act on."
                    ),
                    color=MUTED,
                    font_size="1.12rem",
                    line_height="1.75",
                    max_width="760px",
                    text_align="center",
                ),
                align="center",
                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="5.5rem 0 4rem",
            background=BACKGROUND,
        ),

        # Mission, audience and principle
        rx.box(
            rx.flex(
                information_card(
                    "OUR MISSION",
                    "Turn energy data into useful action",
                    (
                        "Smart meters generate valuable information, but "
                        "consumption charts rarely explain what someone "
                        "should do next. Volti bridges that gap."
                    ),
                    dark=True,
                ),
                information_card(
                    "WHO IT IS FOR",
                    "Built for real households",
                    (
                        "Volti is designed for busy households that want "
                        "to reduce energy costs without spending hours "
                        "analysing tariffs or technical data."
                    ),
                ),
                information_card(
                    "OUR PRINCIPLE",
                    "Privacy conscious",
                    (
                        "Energy information should be handled transparently "
                        "and used only for relevant insights."
                    ),
                    soft=True,
                ),
                gap="1.5rem",
                align="stretch",
                flex_wrap="wrap",
                **PAGE_CONTAINER,
            ),
            padding="5rem 0",
            background=SURFACE,
        ),

        # Team
        rx.box(
            rx.vstack(
                rx.box(
                    rx.text(
                        "OUR TEAM",
                        color=ACCENT,
                        font_size="0.8rem",
                        font_weight="800",
                        letter_spacing="0.16em",
                    ),
                    padding="0.5rem 1rem",
                    background="rgba(22,135,126,0.08)",
                    border="1px solid rgba(22,135,126,0.18)",
                    border_radius="999px",
                ),
                rx.heading(
                    "Meet the people behind Volti",
                    size="8",
                    color=PRIMARY,
                    letter_spacing="-0.035em",
                    text_align="center",
                ),
                rx.text(
                    (
                        "A multidisciplinary team working together to turn "
                        "complex household energy data into clear and useful action."
                    ),
                    color=MUTED,
                    font_size="1.05rem",
                    line_height="1.75",
                    max_width="720px",
                    text_align="center",
                ),
                rx.flex(
                    *[
                        team_member_card(**member)
                        for member in TEAM_MEMBERS
                    ],
                    width="100%",
                    justify="center",
                    align="stretch",
                    gap="1.5rem",
                    flex_wrap="wrap",
                    margin_top="1.5rem",
                ),
                align="center",
                spacing="5",
                **PAGE_CONTAINER,
            ),
            padding="5.5rem 0 6rem",
            background=BACKGROUND,
        ),

        min_height="100vh",
        background=BACKGROUND,
    )