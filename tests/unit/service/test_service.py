import pytest
from now8_api.service import CityNameError
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData
from now8_api.service.service import assign_city_data


class TestAssignCityStop:
    def test_assign_city_data(self):
        result = assign_city_data(city_name="Madrid")

        assert isinstance(result, CityData)
        assert isinstance(result, MadridCityData)

    def test_assign_city_stop_raises(self):
        with pytest.raises(CityNameError):
            assign_city_data(city_name="fake_city")
