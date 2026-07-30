import os
import reflex as rx

# Render veya deployment ortamından portları ve URL'leri al
port = os.getenv("PORT")
frontend_port = int(port) if port is not None else 3000
backend_port = int(port) if port is not None else 8001

# Backend canlı URL'i (Örn: https://yzta-bootcamp-304-1.onrender.com)
api_url = os.getenv("API_URL", f"http://127.0.0.1:{backend_port}")
deploy_url = os.getenv("DEPLOY_URL", f"http://127.0.0.1:{frontend_port}")

config = rx.Config(
    app_name="reflex_frontend",
    frontend_port=frontend_port,
    backend_port=backend_port,
    backend_host="0.0.0.0",
    api_url=api_url,
    deploy_url=deploy_url,
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


# import os
# import reflex as rx


# config = rx.Config(
#     app_name="reflex_frontend",
#     frontend_port=3000,
#     backend_port=8001,
#     backend_host="0.0.0.0",
#     api_url=os.getenv("API_URL", "http://127.0.0.1:8001"),
#     deploy_url=os.getenv("DEPLOY_URL", "http://127.0.0.1:3000"),
#     plugins=[
#         rx.plugins.SitemapPlugin(),
#         rx.plugins.RadixThemesPlugin(
#             theme=rx.theme(
#                 appearance="light",
#                 accent_color="teal",
#             )
#         ),
#     ],
# )