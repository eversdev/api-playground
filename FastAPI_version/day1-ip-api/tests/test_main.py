from fastapi.testclient import TestClient

from src.main import app


def test_home_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == '"Hello world"'


def test_greeting_endpoint():
    with TestClient(app) as client:
        response = client.get("/hello/john")
        assert response.status_code == 200
        assert response.json() == {"hello": "john"}
        
