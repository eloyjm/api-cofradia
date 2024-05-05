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

def test_get_hermandades(client_logged_in):
    response = client_logged_in.get("/hermandades")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_hermandades_by_day(client_logged_in):
    response = client_logged_in.get("/hermandades/day/Domingo%20de%20Ramos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_hermandades_by_id(client_logged_in):
    response = client_logged_in.get("/hermandades/1538b1d6-35aa-4a25-954f-3ac896877f95")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_parse_wiki(client_logged_in):
    response = client_logged_in.patch("/migrate/wiki")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_parse_wiki_day(client_logged_in):
    response = client_logged_in.patch("/migrate/wiki/day/Domingo%20de%20Ramos")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_parse_wiki_by_id(client_logged_in):
    response = client_logged_in.patch("/migrate/wiki/1538b1d6-35aa-4a25-954f-3ac896877f95")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_hermandad_image_escudo(client_logged_in):
    response = client_logged_in.get("/hermandades/1538b1d6-35aa-4a25-954f-3ac896877f95/image/escudo")
    assert response.status_code == 200

def test_get_hermandad_image_traje(client_logged_in):
    response = client_logged_in.get("/hermandades/1538b1d6-35aa-4a25-954f-3ac896877f95/image/traje")
    assert response.status_code == 200