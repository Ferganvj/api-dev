"""End-to-end tests using FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

VALID_TOKEN = "demo_token"
VALID_API_KEY = "portfolio_showcase_key"


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_token(client):
    resp = client.post("/token")
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"] == VALID_TOKEN
    assert body["token_type"] == "bearer"


def test_analyze_text_basic(client):
    resp = client.post(
        "/analyze-text",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"},
        json={"text": "hello world hello", "analysis_type": "basic"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["word_count"] == 3
    assert body["unique_words"] == 2
    assert body["character_count"] == len("hello world hello")
    assert body["sentiment_score"] is None
    assert body["processing_time_ms"] >= 0


def test_analyze_text_advanced_has_sentiment(client):
    resp = client.post(
        "/analyze-text",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"},
        json={"text": "great great excellent", "analysis_type": "advanced"},
    )
    assert resp.status_code == 200
    assert resp.json()["sentiment_score"] > 0


def test_analyze_text_requires_auth(client):
    resp = client.post("/analyze-text", json={"text": "no token"})
    assert resp.status_code == 401
    assert resp.json()["error"] == "Invalid access token"


def test_analyze_text_rejects_bad_token(client):
    resp = client.post(
        "/analyze-text",
        headers={"Authorization": "Bearer nope"},
        json={"text": "bad token"},
    )
    assert resp.status_code == 401


def test_analyze_text_validation_error(client):
    resp = client.post(
        "/analyze-text",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"},
        json={"text": "", "analysis_type": "basic"},
    )
    assert resp.status_code == 422


def test_health_requires_api_key(client):
    resp = client.get("/system/health")
    assert resp.status_code == 401
    assert resp.json()["error"] == "Invalid API Key"


def test_health_with_api_key(client):
    resp = client.get("/system/health", headers={"X-API-KEY": VALID_API_KEY})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "operational"
    assert body["version"] == "2.1.0"
    assert body["uptime_seconds"] >= 0
    assert body["active_requests"] >= 0
