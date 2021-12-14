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
            "latitude": pytest.approx(40.242103577),
            "longitude": pytest.approx(-4.190074921),
            "name": "MÉNTRIDA-ESTACIÓN DE SERVICIO",
            "route_ways": [
                {"id": "358", "way": 0},
                {"id": "235", "way": 0},
                {"id": "141", "way": 1},
                {"id": "252", "way": 0},
                {"id": "137", "way": 0},
                {"id": "527", "way": 1},
                {"id": "136", "way": 1},
                {"id": "107", "way": 0},
                {"id": "250", "way": 0},
            ],
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
            "latitude": pytest.approx(40.295986176),
            "longitude": pytest.approx(-3.457196951),
            "name": "RONDA SUR-HOSPITAL DEL SURESTE",
            "route_ways": [{"id": "278", "way": 1}],
            "zone": "B3",
        }


class TestStopEstimation:
    def test_madrid_estimation(self, client):
        response = client.get("/stop/par_8_17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
