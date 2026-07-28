import reflex as rx

from .pages.about import about
from .pages.dashboard import dashboard
from .pages.home import home
from .pages.how_it_works import how_it_works
from .state import DashboardState

app = rx.App(
    stylesheets=[
        "/animations.css",
    ],
)

app.add_page(
    home,
    route="/",
    title="Volti | Smart Energy Coach",
)

app.add_page(
    dashboard,
    route="/dashboard",
    title="Dashboard | Volti",
    on_load=DashboardState.initialize_page,
)

app.add_page(
    how_it_works,
    route="/how-it-works",
    title="How It Works | Volti",
)

app.add_page(
    about,
    route="/about",
    title="About | Volti",
)