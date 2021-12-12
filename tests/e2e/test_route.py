import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api.main import api


class TestRoute:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_route(self):
        response = self.client.get("/route")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestRouteInfo:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_madrid_route(self):
        response = self.client.get("/route/633/info")

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
