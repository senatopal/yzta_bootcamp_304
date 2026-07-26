import reflex as rx


config = rx.Config(
    app_name="reflex_frontend",
    frontend_port=3000,
    backend_port=8001,
    backend_host="0.0.0.0",
    api_url="http://127.0.0.1:8001",
    deploy_url="http://127.0.0.1:3000",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="light",
                accent_color="teal",
            )
        ),
    ],
)