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
        assert response.json()["par_8_99987"]["code"] == "99987"
        assert response.json()["par_8_99987"]["id"] == "par_8_99987"
        assert response.json()["par_8_99987"]["latitude"] == pytest.approx(
            40.242103577
        )
        assert response.json()["par_8_99987"]["longitude"] == pytest.approx(
            -4.190074921
        )
        assert (
            response.json()["par_8_99987"]["name"]
            == "MÉNTRIDA-ESTACIÓN DE SERVICIO"
        )
        assert all(
            (
                isinstance(route_way, dict)
                and isinstance(route_way["id"], str)
                and isinstance(route_way["way"], int)
            )
            for route_way in response.json()["par_8_99987"]["route_ways"]
        )
        assert {"id": "8__541___", "way": 0} in response.json()["par_8_99987"][
            "route_ways"
        ]

        assert response.json()["par_8_99987"]["zone"] == "E1"


class TestStopInfo:
    def test_madrid_stop(self, client):
        response = client.get("/stop/par_8_17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["code"] == "17491"
        assert response.json()["id"] == "par_8_17491"
        assert response.json()["latitude"] == pytest.approx(40.295986176)
        assert response.json()["longitude"] == pytest.approx(-3.457196951)
        assert response.json()["name"] == "RONDA SUR-HOSPITAL DEL SURESTE"
        assert all(
            (
                isinstance(route_way, dict)
                and isinstance(route_way["id"], str)
                and isinstance(route_way["way"], int)
            )
            for route_way in response.json()["route_ways"]
        )
        assert {"id": "8__330___", "way": 0} in response.json()["route_ways"]
        assert response.json()["zone"] == "B3"


class TestStopEstimation:
    def test_madrid_estimation(self, client):
        response = client.get("/stop/par_8_17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
