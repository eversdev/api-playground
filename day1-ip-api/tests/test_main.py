from src.main import app

import pytest

def test_home_endpoint():
    with app.test_client() as client:
        response = client.get("/")
        assert response.data.decode("utf-8") == "<h1>Hello World</h1>"
        assert response.status_code == 200


def test_greet_endpoint():
    with app.test_client() as client:
        response = client.get("/greet/John")
        assert response.data.decode("utf-8") == "Hello John!"
        assert response.status_code == 200

