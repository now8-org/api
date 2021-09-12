from now8_api.domain import TransportType
from now8_api.service.city_data.madrid import _stop_id_api, _stop_id_user


class TestFunctions:
    def test_stop_id_user(self):
        result = _stop_id_user(
            stop_id_api="8_test_id_api",
            transport_type=TransportType.INTERCITY_BUS,
        )
        assert result == "test_id_api"

    def test_stop_id_api(self):
        result = _stop_id_api(
            stop_id_user="test_id_api",
            transport_type=TransportType.INTERCITY_BUS,
        )
        assert result == "8_test_id_api"
