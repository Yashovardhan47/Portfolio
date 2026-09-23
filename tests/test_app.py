import tempfile
from pathlib import Path

import pytest

from portfolio import create_app


@pytest.fixture()
def client():
    with tempfile.TemporaryDirectory() as temp_dir:
        app = create_app(
            {
                "TESTING": True,
                "DATABASE": str(Path(temp_dir) / "test.db"),
                "SITE_URL": "https://portfolio.example",
            }
        )
        yield app.test_client()


def test_home_renders_current_projects(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"BillFlow AI" in response.data
    assert b"OmniCalc + CalcGraph" in response.data
    assert b"Quick Hire" in response.data


def test_health_and_projects_api(client):
    health = client.get("/api/health")
    assert health.get_json() == {"service": "portfolio", "status": "ok"}
    projects = client.get("/api/projects").get_json()["projects"]
    assert len(projects) >= 6
    assert all(item["github"].startswith("https://github.com/") for item in projects)


def test_assistant_is_grounded(client):
    response = client.post("/api/assistant", json={"question": "Which project uses FastAPI?"})
    assert response.status_code == 200
    result = response.get_json()
    assert result["grounded"] is True
    assert result["sources"]
    assert "FastAPI" in result["answer"]


def test_contact_validates_and_persists(client):
    invalid = client.post("/api/contact", json={"name": "Y", "email": "bad", "message": "x"})
    assert invalid.status_code == 400

    valid = client.post(
        "/api/contact",
        json={
            "name": "Recruiter Example",
            "email": "recruiter@example.com",
            "subject": "Python role",
            "message": "I would like to discuss a Python engineering opportunity.",
        },
        headers={"X-Forwarded-For": "203.0.113.9"},
    )
    assert valid.status_code == 201
    assert valid.get_json()["reference"].startswith("MSG-")


def test_seo_endpoints(client):
    assert b"Sitemap:" in client.get("/robots.txt").data
    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    assert b"https://portfolio.example/" in sitemap.data
