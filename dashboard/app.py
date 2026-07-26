from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Volti",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css() -> None:
    css_path = Path(__file__).parent / "style.css"

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


load_css()


pages = [
    st.Page(
        "pages/home.py",
        title="Home",
        icon=":material/home:",
        default=True,
    ),
    st.Page(
        "pages/dashboard.py",
        title="Dashboard",
        icon=":material/dashboard:",
    ),
    st.Page(
        "pages/how_it_works.py",
        title="How It Works",
        icon=":material/bolt:",
    ),
    st.Page(
        "pages/about.py",
        title="About",
        icon=":material/info:",
    ),
]

navigation = st.navigation(
    pages,
    position="top",
)

navigation.run()