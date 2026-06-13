import os

os.environ["AUTO_CREATE_TABLES"] = "false"

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.routers import analysis_router
from main import app


def _fake_db():
    """Provide a fake dependency value for route tests."""
    yield object()


def test_avg_price_analysis_response_shape(monkeypatch):
    """Analysis API should return chart-ready labels and values."""
    app.dependency_overrides[get_db] = _fake_db
    monkeypatch.setattr(
        analysis_router,
        "avg_price_by_district",
        lambda db, city=None: {"labels": ["浦东"], "values": [65000]},
    )
    client = TestClient(app)

    response = client.get("/api/analysis/avg-price-by-district")

    assert response.status_code == 200
    assert response.json() == {"labels": ["浦东"], "values": [65000]}
    app.dependency_overrides.clear()
