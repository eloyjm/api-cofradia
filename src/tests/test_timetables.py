import pytest
from fastapi.testclient import TestClient
from ..main import app

@pytest.fixture(scope="module")
def client_logged_in():
    client = TestClient(app)
    response = client.post("/login", data={"username": "eloyjm93@gmail.com", "password": "q"})
    print(response.json())
    token = response.json().get("access_token")
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_get_timetables(client_logged_in):
    response = client_logged_in.get("/timetables")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_timetables_by_hermandad(client_logged_in):
    response = client_logged_in.get("/timetables/hermandades/1538b1d6-35aa-4a25-954f-3ac896877f95")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_migrate_timetables(client_logged_in):
    response = client_logged_in.post("/timetables/migrate/all")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_migrate_timetables_by_day(client_logged_in):
    response = client_logged_in.post("/timetables/migrate/day/Domingo%20de%20Ramos")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_migrate_timetables_by_id(client_logged_in):
    response = client_logged_in.post("/timetables/migrate/1538b1d6-35aa-4a25-954f-3ac896877f95")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)