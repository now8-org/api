from typing import List

import pytest
from now8_api.service.service import Service
from tests.conftest import FakeCityData, FakeSqlEngine


class TestService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = Service(
            city_data=FakeCityData(),
            sql_engine=FakeSqlEngine(),
        )

    stop_keys: List[str] = [
        "code",
        "name",
        "longitude",
        "latitude",
        "zone",
        "lines",
    ]

    @pytest.mark.asyncio
    async def test_all_stops_structure(self):
        result = await self.service.all_stops()

        assert isinstance(result, dict)
        assert all(isinstance(item, dict) for item in result.values())
        assert all(
            isinstance(value, (str, float, dict))
            for d in result.values()
            for value in d.values()
        )
        assert all(list(d.keys()) == self.stop_keys for d in result.values())

    @pytest.mark.asyncio
    async def test_all_stops_lines(self):
        result = await self.service.all_stops()

        assert all(
            list(line.keys())
            == [
                "name",
                "code",
                "transport_type",
                "color",
                "way",
            ]
            for stop in result.values()
            for line in stop["lines"].values()
        )

    @pytest.mark.parametrize("exclude", stop_keys)
    @pytest.mark.asyncio
    async def test_all_stops_exclude(self, exclude):
        result = await self.service.all_stops(exclude=[exclude])

        assert all(
            list(d.keys()) == [key for key in self.stop_keys if key != exclude]
            for d in result.values()
        )

    @pytest.mark.asyncio
    async def test_all_stops_exclude_multiple(self):
        result = await self.service.all_stops(exclude=self.stop_keys[:2])

        assert all(
            list(d.keys())
            == [key for key in self.stop_keys if key not in self.stop_keys[:2]]
            for d in result.values()
        )

    @pytest.mark.asyncio
    async def test_stop_info(self):
        result = await self.service.stop_info(stop_id="1_42")

        assert isinstance(result, dict)
        assert all(isinstance(key, str) for key in result.keys())
        assert all(
            isinstance(value, (str, float, dict)) for value in result.values()
        )
        assert result == {
            "code": "42",
            "name": "Stop 42",
            "longitude": 0.0,
            "latitude": 0.0,
            "zone": "A",
            "lines": {
                "route_id_1": {
                    "code": "route_short_name_1",
                    "color": "#0f0",
                    "name": "route_long_name_1",
                    "transport_type": 3,
                    "way": 0,
                },
                "route_id_2": {
                    "code": "route_short_name_2",
                    "color": "#f00",
                    "name": "route_long_name_2",
                    "transport_type": 3,
                    "way": 1,
                },
            },
        }
