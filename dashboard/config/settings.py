import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "VOLTI_API_URL",
    "http://localhost:8000/api/v1",
).rstrip("/")

API_TIMEOUT = int(os.getenv("VOLTI_API_TIMEOUT", "15"))