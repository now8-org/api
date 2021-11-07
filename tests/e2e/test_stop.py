import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api.main import api


class TestStop:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_stop(self):
        response = self.client.get("/stop")

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestStopInfo:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_stop(self):
        response = self.client.get("/stop/17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestStopEstimation:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_estimation(self):
        response = self.client.get("/stop/17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
