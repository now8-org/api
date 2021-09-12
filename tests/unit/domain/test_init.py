from datetime import datetime

from now8_api.domain import Estimation, Line, Vehicle


class TestLine:
    def test_line_default_name(self):
        line_id = "test_line_id"
        line = Line(id=line_id)

        assert line.name == line_id


class TestVehicle:
    def test_vehicle_default_name(self):
        vehicle_id = "test_vehicle_id"
        line = Line(id="test_line")
        vehicle = Vehicle(id=vehicle_id, line=line)

        assert vehicle.name == vehicle_id


class TestEstimation:
    def test_estimation_default_time(self):
        estimation = datetime(3000, 1, 1)
        estimation = Estimation(estimation=estimation)

        assert isinstance(estimation.time, datetime)
