from typing import List, Tuple

import pytest
from now8_api.domain import Stop, VehicleEstimation
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData


class TestCities:

    cities_transport_types: List[Tuple[CityData, Stop]] = [
        (
            MadridCityData(),
            Stop(id="par_8_17491"),
        ),
        (
            MadridCityData(),
            Stop(id="par_6_4285"),
        ),
        (
            MadridCityData(),
            Stop(id="par_5_11"),
        ),
    ]

    @pytest.mark.slow
    @pytest.mark.asyncio
    @pytest.mark.parametrize("city_data,stop", cities_transport_types)
    async def test_get_estimations(self, city_data, stop):
        result = await city_data.get_estimations(stop)

        assert isinstance(result, list)
        assert all(isinstance(item, VehicleEstimation) for item in result)
        assert all(
            vehicle_estimation.vehicle.id != ""
            for vehicle_estimation in result
        )
        assert all(
            vehicle_estimation.vehicle.name != ""
            for vehicle_estimation in result
        )
