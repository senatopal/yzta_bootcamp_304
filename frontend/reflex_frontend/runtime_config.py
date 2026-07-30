import os

DEFAULT_RENDER_BACKEND_ROOT = "https://yzta-bootcamp-304-1.onrender.com"


def resolve_backend_root() -> str:
    """Resolve the FastAPI backend root from environment variables.

    Supports the Render deployment names used in this project and strips
    trailing API path segments when the variable already contains /api or /api/v1.
    """

    candidates = [
        os.getenv("FASTAPI_ROOT"),
        os.getenv("BACKEND_URL"),
        os.getenv("API_URL"),
        os.getenv("BACKEND_API_URL"),
    ]

    for candidate in candidates:
        if not candidate:
            continue

        value = candidate.strip().rstrip("/")
        if value.endswith("/api/v1"):
            return value[: -len("/api/v1")]
        if value.endswith("/api"):
            return value[: -len("/api")]
        return value

    if os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_URL"):
        return DEFAULT_RENDER_BACKEND_ROOT

    return "http://127.0.0.1:8000"
