from typing import List, Tuple

import pytest
from ntapi import City, Stop, TransportType
from ntapi.data.cities.madrid import MadridCity, MadridStop


class TestCities:

    cities_transport_types: List[Tuple[City, Stop]] = [
        (
            MadridCity(),
            MadridStop(
                id_api="8_17491", transport_type=TransportType.INTERCITY_BUS
            ),
        )
    ]

    @pytest.mark.slow
    @pytest.mark.asyncio
    @pytest.mark.parametrize("city,stop", cities_transport_types)
    async def test_get_estimations(self, city, stop):
        result = await city.get_estimations(stop)

        assert len(result) > 0
