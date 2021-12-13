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
            "code": "6",
            "color": "E60003",
            "id": "999",
            "name": "UNIVERSIDAD REY JUAN CARLOS-URB. P.GUADARRAMA",
            "transport_type": 3,
        }


class TestRouteInfo:
    def test_madrid_route(self, client):
        response = client.get("/route/633/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json() == {
            "code": "151",
            "color": "8EBF42",
            "id": "633",
            "name": "MADRID (Plaza de Castilla) - ALCOBENDAS",
            "transport_type": 3,
        }
