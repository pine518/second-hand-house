import os

os.environ["AUTO_CREATE_TABLES"] = "false"

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.routers import api_router
from main import app


def _fake_db():
    """Provide a fake dependency value for route tests."""
    yield object()


def test_api_list_houses_response_shape(monkeypatch):
    """House list API should expose pagination metadata."""
    app.dependency_overrides[get_db] = _fake_db

    def fake_list_houses(*args, **kwargs):
        return {"items": [], "total": 0, "page": 1, "page_size": 20, "pages": 1}

    monkeypatch.setattr(api_router, "list_houses", fake_list_houses)
    client = TestClient(app)

    response = client.get("/api/houses")

    assert response.status_code == 200
    assert response.json()["pages"] == 1
    app.dependency_overrides.clear()
