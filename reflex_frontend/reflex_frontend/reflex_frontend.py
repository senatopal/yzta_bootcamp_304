import reflex as rx

from .pages.about import about
from .pages.dashboard import dashboard
from .pages.home import home
from .pages.how_it_works import how_it_works


app = rx.App()

app.add_page(
    home,
    route="/",
    title="Volti | Smart Energy Coach",
)

app.add_page(
    dashboard,
    route="/dashboard",
    title="Dashboard | Volti",
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