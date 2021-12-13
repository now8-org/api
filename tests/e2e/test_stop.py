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


class TestStopInfo:
    def test_madrid_stop(self, client):
        response = client.get("/stop/par_8_17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestStopEstimation:
    def test_madrid_estimation(self, client):
        response = client.get("/stop/par_8_17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
