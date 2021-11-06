import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api.main import api


class TestStopMadrid:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_stop(self):
        response = self.client.get("/stop/madrid")

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestStopInfoMadrid:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_stop(self):
        response = self.client.get("/stop/madrid/17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestStopEstimationMadrid:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_estimation(self):
        response = self.client.get("/stop/madrid/17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
