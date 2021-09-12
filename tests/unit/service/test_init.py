import pytest
from now8_api.service import CityNameError, StopIdError, TransportTypeError


class TestErrors:
    def test_city_name_error(self):
        city_name = "test_city_name"

        with pytest.raises(CityNameError) as error:
            raise CityNameError(city_name=city_name)

        assert city_name in str(error.value)

    def test_transport_type_error(self):
        transport_type = "test_transport_type"

        with pytest.raises(TransportTypeError) as error:
            raise TransportTypeError(transport_type=transport_type)

        assert transport_type in str(error.value)

    def test_raise_stop_id_error(self):
        stop_id = "test_stop_id"

        with pytest.raises(StopIdError) as error:
            raise StopIdError(stop_id=stop_id)

        assert stop_id in str(error.value)
