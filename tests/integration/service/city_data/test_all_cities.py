from typing import List, Tuple

import pytest
from now8_api.domain import Stop, TransportType, VehicleEstimation
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData


class TestCities:

    cities_transport_types: List[Tuple[CityData, Stop]] = [
        (
            MadridCityData(),
            Stop(id="17491", transport_type=TransportType.INTERCITY_BUS),
        )
    ]

    @pytest.mark.slow
    @pytest.mark.asyncio
    @pytest.mark.parametrize("city_data,stop", cities_transport_types)
    async def test_get_estimations(self, city_data, stop):
        result = await city_data.get_estimations(stop)

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(item, VehicleEstimation) for item in result)
