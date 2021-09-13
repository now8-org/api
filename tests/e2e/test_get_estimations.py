import pytest
from fastapi.testclient import TestClient
from now8_api.entrypoints.api import api


class TestGetEstimationsMadrid:
    @pytest.fixture(autouse=True)
    def initialize_test_client(self):
        self.client = TestClient(api)

    def test_get_estimations_intercity_bus(self):
        response = self.client.get("/madrid/get_estimations?stop_id=17491")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
