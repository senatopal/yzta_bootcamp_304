import os
import reflex as rx

port = int(os.getenv("PORT", 3000))

config = rx.Config(
    app_name="reflex_frontend",
    frontend_port=port,
    backend_port=port,  
    backend_host="0.0.0.0",
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