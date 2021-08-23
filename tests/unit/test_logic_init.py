from unittest.mock import Mock, patch

import pytest
from ntapi import City, CityNameError, Stop
from ntapi.logic import assign_city_stop, get_estimations


class TestAssignCityStop:
    @patch.multiple(City, __abstractmethods__=set())
    @patch.multiple(Stop, __abstractmethods__=set())
    def test_assign_city_stop(self):
        cities_stops = {"Test": (City, Stop)}
        result = assign_city_stop("test", cities_stops)

        assert isinstance(result, tuple)
        assert result[0] == City
        assert result[1] == Stop

    def test_assign_city_stop_raises(self):
        with pytest.raises(CityNameError):
            assign_city_stop("fake_city")


class TestGetEstimations:
    @patch.multiple(
        City, __abstractmethods__=set(), get_estimations=Mock(return_value=[])
    )
    @patch.multiple(Stop, __abstractmethods__=set())
    @patch("ntapi.logic.assign_city_stop", return_value=(City, Stop))
    def test_get_estimations(self, mock_assign_city_stop):
        city_name = "test_city"
        id_user = "test_id"

        result = get_estimations(city_name, {"id_user": id_user})

        mock_assign_city_stop.assert_called_once_with(city_name)
        assert result == []

    @patch.multiple(
        City,
        __abstractmethods__=set(),
        get_estimations=Mock(side_effect=NotImplementedError),
    )
    @patch.multiple(Stop, __abstractmethods__=set())
    @patch("ntapi.logic.assign_city_stop", return_value=(City, Stop))
    def test_get_estimations_raises(self, mock_assign_city_stop):
        city_name = "test_city"
        id_user = "test_id"

        with pytest.raises(NotImplementedError):
            get_estimations(city_name, {"id_user": id_user})

        mock_assign_city_stop.assert_called_once_with(city_name)
