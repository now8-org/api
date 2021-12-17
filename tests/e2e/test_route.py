import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api.main import api


@pytest.fixture
def client():
    with TestClient(api) as client:
        yield client


class TestRoute:
    def test_route(self, client):
        response = client.get("/route")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["8__483___"] == {
            "id": "8__483___",
            "code": "483",
            "name": "MADRID (Aluche)-LEGANÉS (Vereda de los Estudiantes)",
            "transport_type": 3,
            "color": "8EBF42",
        }


class TestRouteInfo:
    def test_madrid_route(self, client):
        response = client.get("/route/10__ML2___/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json() == {
            "id": "10__ML2___",
            "code": "ML2",
            "name": "Colonia Jardín - Estación de Aravaca",
            "transport_type": 0,
            "color": "A60084",
        }
