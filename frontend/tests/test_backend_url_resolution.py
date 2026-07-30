import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reflex_frontend.runtime_config import resolve_backend_root


def test_prefers_fastapi_root_when_present(monkeypatch):
    monkeypatch.setenv("FASTAPI_ROOT", "https://backend.example.com")
    monkeypatch.delenv("API_URL", raising=False)
    monkeypatch.delenv("BACKEND_URL", raising=False)
    monkeypatch.delenv("RENDER", raising=False)

    assert resolve_backend_root() == "https://backend.example.com"


def test_uses_render_backend_default_when_available(monkeypatch):
    monkeypatch.delenv("FASTAPI_ROOT", raising=False)
    monkeypatch.delenv("API_URL", raising=False)
    monkeypatch.delenv("BACKEND_URL", raising=False)
    monkeypatch.setenv("RENDER", "true")

    assert resolve_backend_root() == "https://yzta-bootcamp-304-1.onrender.com"
