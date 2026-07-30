# Previous implementation kept for reference:
# import os
# import reflex as rx
#
# port = os.getenv("PORT")
# frontend_port = int(port) if port is not None else 3000
# backend_port = int(port) if port is not None else 8001
#
# default_deploy_url = f"http://127.0.0.1:{frontend_port}"
#
# config = rx.Config(
#     app_name="reflex_frontend",
#     frontend_port=frontend_port,
#     backend_port=backend_port,
#     backend_host="0.0.0.0",
#     api_url=os.getenv("API_URL", "http://127.0.0.1:8001"),
#     deploy_url=os.getenv("DEPLOY_URL", default_deploy_url),
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

import os
import reflex as rx

from reflex_frontend.runtime_config import resolve_backend_root

port = os.getenv("PORT")
frontend_port = int(port) if port is not None else 3000
backend_port = int(port) if port is not None else 8001


frontend_root = os.getenv("FRONTEND_ROOT", os.getenv("RENDER_EXTERNAL_URL"))
default_deploy_url = frontend_root or f"http://127.0.0.1:{frontend_port}"

config = rx.Config(
    app_name="reflex_frontend",
    frontend_port=frontend_port,
    backend_port=backend_port,
    backend_host="0.0.0.0",
    api_url=frontend_root or os.getenv("API_URL", default_deploy_url),
    deploy_url=os.getenv("DEPLOY_URL", default_deploy_url),
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