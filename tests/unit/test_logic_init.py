from unittest.mock import AsyncMock, Mock, patch

import pytest
from now8_api import City, CityNameError, Stop
from now8_api.data.cities.madrid import MadridCity, MadridStop
from now8_api.logic import (
    Cities,
    CitiesStops,
    assign_city_stop,
    get_estimations,
)


class TestAssignCityStop:
    @patch.multiple(City, __abstractmethods__=set())
    @patch.multiple(Stop, __abstractmethods__=set())
    def test_assign_city_stop(self):
        cities_stops: CitiesStops = {Cities.MADRID: (MadridCity, MadridStop)}
        result = assign_city_stop("Madrid", cities_stops)

        assert isinstance(result, tuple)
        assert result[0] == MadridCity
        assert result[1] == MadridStop

    def test_assign_city_stop_raises(self):
        with pytest.raises(CityNameError):
            assign_city_stop("fake_city")


class TestGetEstimations:
    @patch.multiple(
        City,
        __abstractmethods__=set(),
        get_estimations=AsyncMock(return_value=[]),
    )
    @patch.multiple(Stop, __abstractmethods__=set())
    @patch("now8_api.logic.assign_city_stop", return_value=(City, Stop))
    @pytest.mark.asyncio
    async def test_get_estimations(self, mock_assign_city_stop):
        city_name = "test_city"
        id_user = "test_id"

        result = await get_estimations(city_name, {"id_user": id_user})

        mock_assign_city_stop.assert_called_once_with(city_name)
        assert result == []

    @patch.multiple(
        City,
        __abstractmethods__=set(),
        get_estimations=Mock(side_effect=NotImplementedError),
    )
    @patch.multiple(Stop, __abstractmethods__=set())
    @patch("now8_api.logic.assign_city_stop", return_value=(City, Stop))
    @pytest.mark.asyncio
    async def test_get_estimations_raises(self, mock_assign_city_stop):
        city_name = "test_city"
        id_user = "test_id"

        with pytest.raises(NotImplementedError):
            await get_estimations(city_name, {"id_user": id_user})

        mock_assign_city_stop.assert_called_once_with(city_name)
