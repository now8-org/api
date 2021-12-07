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
        assert isinstance(response.json(), dict)

    def test_stop_exclude_effect(self):
        response_original = self.client.get("/stop")
        response_exclude = self.client.get("/stop?exclude=name&exclude=lines")

        assert response_original.json() != response_exclude.json()


class TestStopInfo:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_stop(self):
        response = self.client.get("/stop/par_8_17491/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestStopEstimation:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_estimation(self):
        response = self.client.get("/stop/par_8_17491/estimation")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
