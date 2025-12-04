import pytest


from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from unittest.mock import patch, Mock, MagicMock


from fastapi_version.main import app

@pytest.fixture
def client():
    return TestClient(app)


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


def test_add_user_creates_db_record():
    with patch("fastapi_version.main.psycopg2.connect") as mock_connect, \
         patch.dict("os.environ", {
             "POSTGRES_USER": "testuser",
             "POSTGRES_PASSWORD": "testpass",
             "POSTGRES_DB": "testdb"
         }):

        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_connection

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.return_value = None

        client = TestClient(app)
        payload = {"first_name": "Alice", "department_id": 1}
        response = client.post("/add_user", json=payload)

        assert response.status_code == 200
        mock_cursor.execute.assert_called()   # ensure SQL execute was called
        mock_connection.commit.assert_called()  # ensure commit was called


