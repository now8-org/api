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
        assert response.json()["999"] == {
            "code": "5",
            "color": "E60003",
            "id": "999",
            "name": "S. S. DE LOS REYES-ALCOBENDAS-SOTO MORALEJA",
            "transport_type": 3,
        }


class TestRouteInfo:
    def test_madrid_route(self, client):
        response = client.get("/route/633/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json() == {
            "code": "ML2",
            "color": "A60084",
            "id": "633",
            "name": "Colonia Jardín - Estación de Aravaca",
            "transport_type": 0,
        }
