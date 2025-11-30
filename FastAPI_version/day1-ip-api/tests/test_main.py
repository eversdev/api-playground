from fastapi.testclient import TestClient

from fastapi_version.main import app


def test_home_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world"}


def test_greeting_endpoint():
    with TestClient(app) as client:
        response = client.get("/hello/john")
        assert response.status_code == 200
        assert response.json() == {"hello": "john"}
        


def test_calculate_sum():
    with TestClient(app) as client:
        response = client.get("/sum?a=1&b=2")
        assert response.status_code == 200
        assert response.json() == {"sum": 3}

