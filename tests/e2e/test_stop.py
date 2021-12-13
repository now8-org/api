import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api.main import api


@pytest.fixture
def client():
    with TestClient(api) as client:
        yield client


class TestStop:
    def test_madrid_stop(self, client):
        response = client.get("/stop")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["par_8_99987"] == {
            "code": "99987",
            "id": "par_8_99987",
            "latitude": 40.242103577,
            "longitude": -4.190074921,
            "name": "MÉNTRIDA-ESTACIÓN DE SERVICIO",
            "route_ways": [{"id": "358", "way": 0}, {"id": "767", "way": 0}],
            "zone": "E1",
        }


class TestStopInfo:
    def test_madrid_stop(self, client):
        response = client.get("/stop/par_8_17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json() == {
            "code": "17491",
            "id": "par_8_17491",
            "latitude": 40.296051025,
            "longitude": -3.457335711,
            "name": "RONDA SUR-HOSPITAL DEL SURESTE",
            "route_ways": [
                {"id": "269", "way": 0},
                {"id": "279", "way": 1},
                {"id": "280", "way": 1},
                {"id": "281", "way": 1},
                {"id": "678", "way": 0},
                {"id": "688", "way": 1},
                {"id": "689", "way": 1},
                {"id": "690", "way": 1},
            ],
            "zone": "B3",
        }


class TestStopEstimation:
    def test_madrid_estimation(self, client):
        response = client.get("/stop/par_8_17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
