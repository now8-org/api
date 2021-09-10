from datetime import datetime
from typing import List, Optional

import pytest
from now8_api import (
    City,
    Estimation,
    Line,
    Stop,
    StopIdError,
    TransportType,
    TransportTypeError,
    Vehicle,
    VehicleEstimation,
)


class TestLine:
    def test_line_default_id_api(self):
        id_user = "test_id_user"
        line = Line(id_user=id_user)

        assert line.id_user == id_user
        assert line.id_api == id_user

    def test_line_default_id_user(self):
        id_api = "test_id_api"
        line = Line(id_api=id_api)

        assert line.id_api == id_api
        assert line.id_user == id_api

    def test_line_default_ids_missing_raises(self):
        with pytest.raises(ValueError):
            Line()

    def test_line_default_name(self):
        id_user = "test_id_user"
        line = Line(id_user=id_user)

        assert line.name == id_user


class TestVehicle:
    def test_vehicle_default_name(self):
        identifier = "test_identifier"
        line = Line(id_user="test_line")
        vehicle = Vehicle(identifier=identifier, line=line)

        assert vehicle.name == identifier


class TestEstimation:
    def test_estimation_default_time(self):
        estimation = datetime(3000, 1, 1)
        estimation = Estimation(estimation=estimation)

        assert isinstance(estimation.time, datetime)


class TestErrors:
    class CityInherit(City):
        name: str = "Test City"
        transport_types: List[TransportType] = []

        def get_estimations(self, stop: Stop) -> List[VehicleEstimation]:
            pass

        def get_stops(
            self,
            transport_types: Optional[List[TransportType]] = None,
        ) -> List[Stop]:
            pass

    def test_raise_transport_type_error(self):
        transport_type = "test_transport_type"
        city = self.CityInherit()

        with pytest.raises(TransportTypeError) as error:
            raise TransportTypeError(transport_type=transport_type, city=city)

        assert transport_type in str(error.value)
        assert "Test City" in str(error.value)

    def test_raise_stop_id_error(self):
        stop_id = "test_stop_id"

        with pytest.raises(StopIdError) as error:
            raise StopIdError(stop_id=stop_id)

        assert stop_id in str(error.value)
