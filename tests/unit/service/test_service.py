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

    @pytest.mark.asyncio
    async def test_all_stops(self):
        result = await self.service.all_stops()

        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)
        assert all(
            isinstance(value, (str, float))
            for item in result
            for value in item.values()
        )
        assert list(result[0].keys()) == [
            "id",
            "name",
            "longitude",
            "latitude",
            "zone",
        ]

    @pytest.mark.asyncio
    async def test_stop_info(self):
        result = await self.service.stop_info(stop_id="42")

        assert isinstance(result, dict)
        assert all(isinstance(key, str) for key in result.keys())
        assert all(
            isinstance(value, (str, float)) for value in result.values()
        )
        assert result == {
            "id": "42",
            "name": "Stop 42",
            "longitude": 0.0,
            "latitude": 0.0,
            "zone": "A",
        }
