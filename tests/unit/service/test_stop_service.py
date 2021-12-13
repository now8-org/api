from typing import List

import pytest
from now8_api.service.stop_service import StopService
from tests.conftest import FakeCityData, FakeSqlEngine


class TestStopService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.stop_service = StopService(
            city_data=FakeCityData(),
            sql_engine=FakeSqlEngine(),
        )

    stop_keys: List[str] = [
        "id",
        "code",
        "name",
        "longitude",
        "latitude",
        "zone",
        "route_ways",
    ]

    @pytest.mark.asyncio
    async def test_all_stops_structure(self):
        result = await self.stop_service.all_stops()

        assert isinstance(result, dict)
        assert all(isinstance(item, dict) for item in result.values())
        assert all(
            isinstance(value, (str, float, list))
            for d in result.values()
            for value in d.values()
        )
        assert all(list(d.keys()) == self.stop_keys for d in result.values())

    @pytest.mark.asyncio
    async def test_all_stops_routes(self):
        result = await self.stop_service.all_stops()

        # must be dict
        assert all(
            isinstance(route_way, dict)
            for stop in result.values()
            for route_way in stop["route_ways"]
        )
        # the keys of the dict must be strings
        assert all(
            all(
                isinstance(route_ways_key, str)
                for route_ways_key in route_way.keys()
            )
            for stop in result.values()
            for route_way in stop["route_ways"]
        )
        # the value of the id key must be str
        assert all(
            isinstance(route_way["id"], str)
            for stop in result.values()
            for route_way in stop["route_ways"]
        )
        # the value of the way key must be int
        assert all(
            isinstance(route_way["way"], int)
            for stop in result.values()
            for route_way in stop["route_ways"]
        )

    @pytest.mark.asyncio
    async def test_stop_info(self):
        result = await self.stop_service.stop_info(stop_id="1_42")

        assert isinstance(result, dict)
        assert all(isinstance(key, str) for key in result.keys())
        assert all(
            isinstance(value, (str, float, list)) for value in result.values()
        )
        assert result == {
            "id": "1_42",
            "code": "42",
            "name": "Stop 42",
            "longitude": 0.0,
            "latitude": 0.0,
            "zone": "A",
            "route_ways": [
                {"id": "route_id_1", "way": 0},
                {"id": "route_id_2", "way": 1},
            ],
        }
