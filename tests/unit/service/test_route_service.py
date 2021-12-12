from typing import List

import pytest
from now8_api.service.route_service import RouteService
from tests.conftest import FakeCityData, FakeSqlEngine


class TestRouteService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.route_service = RouteService(
            city_data=FakeCityData(),
            sql_engine=FakeSqlEngine(),
        )

    route_keys: List[str] = [
        "id",
        "code",
        "name",
        "transport_type",
        "color",
    ]

    @pytest.mark.asyncio
    async def test_all_routes_structure(self):
        result = await self.route_service.all_routes()

        # result should be a dict
        assert isinstance(result, dict)
        # every value of the main dict must be a dict
        assert all(isinstance(item, dict) for item in result.values())
        # every dict of the main dict values must have the specified keys
        assert all(list(d.keys()) == self.route_keys for d in result.values())
        # every value of previous dicts must be of type str or int
        assert all(
            isinstance(value, (str, int))
            for d in result.values()
            for value in d.values()
        )

    @pytest.mark.asyncio
    async def test_route_info(self):
        result = await self.route_service.route_info(route_id="42")

        # result must be a dict
        assert isinstance(result, dict)
        # all keys of the dict must be of type str
        assert all(isinstance(key, str) for key in result.keys())
        # all values of the dict must be of type str or int
        assert all(isinstance(value, (str, int)) for value in result.values())

        assert result == {
            "id": "42",
            "code": "r42",
            "name": "ROUTE 42",
            "transport_type": 1,
            "color": "#FF0000",
        }
