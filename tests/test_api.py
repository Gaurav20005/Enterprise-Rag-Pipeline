from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Enterprise RAG Pipeline API"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "enterprise-rag-pipeline"


def test_search_endpoint():
    response = client.post(
        "/search",
        json={
            "query": "How many days can employees work remotely?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "query" in data
    assert "results" in data
    assert data["query"] == (
        "How many days can employees work remotely?"
    )
    assert len(data["results"]) > 0


def test_search_validation():
    response = client.post(
        "/search",
        json={
            "query": "",
            "top_k": 3,
        },
    )

    assert response.status_code == 422


def test_search_top_k_validation():
    response = client.post(
        "/search",
        json={
            "query": "What is the annual leave policy?",
            "top_k": 50,
        },
    )

    assert response.status_code == 422