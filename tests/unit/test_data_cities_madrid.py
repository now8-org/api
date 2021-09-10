import pytest
from now8_api import Stop, TransportType
from now8_api.data.cities.madrid import MadridCity, MadridStop
from pydantic import ValidationError


class TestMadridCity:
    class StopInherit(Stop):
        def generate_id_api(cls, value, values):
            pass

        def generate_id_user(cls, value, values):
            pass

    @pytest.mark.asyncio
    async def test_get_estimation_raises_not_implemented(self):
        city = MadridCity()
        stop = self.StopInherit(id_api="test_stop")

        with pytest.raises(NotImplementedError):
            await city.get_estimations(stop)


class TestMadridStop:
    def test_no_ids_raises_value_error(self):
        with pytest.raises(ValueError):
            MadridStop(transport_type=TransportType.INTERCITY_BUS)

    def test_default_id_api(self):
        madrid_stop = MadridStop(
            id_user="test_id_user", transport_type=TransportType.INTERCITY_BUS
        )

        assert madrid_stop.id_api == "8_test_id_user"

    def test_default_id_user(self):
        madrid_stop = MadridStop(
            id_api="8_test_id_api", transport_type=TransportType.INTERCITY_BUS
        )

        assert madrid_stop.id_user == "test_id_api"

    def test_default_ids_raises_transport_type_error(self):
        with pytest.raises(ValidationError):
            MadridStop(
                id_api="test_id_api",
            )

        with pytest.raises(ValidationError):
            MadridStop(
                id_user="test_id_user",
            )
