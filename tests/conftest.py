from typing import List, Optional, Tuple

from overrides import overrides
from pydantic.dataclasses import dataclass

from now8_api.data.database import SqlEngine
from now8_api.domain import Route, Stop, TransportType, VehicleEstimation
from now8_api.service.city_data import CityData


class FakeCityData(CityData):
    @overrides
    async def get_estimations(
        self,
        stop: Stop,
    ) -> List[VehicleEstimation]:
        return []

    @overrides
    async def get_stops_city(
        self,
        transport_types: List[TransportType] = None,
    ) -> List[Stop]:
        return []

    @overrides
    async def get_stops_route(
        self,
        route: Route,
    ) -> Tuple[List[Stop], List[Stop]]:
        return ([], [])

    @overrides
    async def get_routes_stop(
        self,
        stop: Stop,
    ) -> List[Route]:
        return []


@dataclass
class FakeSqlEngine(SqlEngine):
    env_prefix: str = "FAKE_DB_"
    name: Optional[str] = "fake_name"
    user: Optional[str] = "fake_user"
    password: Optional[str] = "fake_password"
    host: Optional[str] = "fake_host"
    port: Optional[str] = "fake_port"

    @overrides
    async def execute_query(self, query: str, *_) -> List[tuple]:
        if (
            query == "SELECT DISTINCT "
            '"route_id","route_short_name","route_long_name",'
            '"route_type","route_color" '
            'FROM "routes"'
        ):
            return [
                ("42", "r42", "ROUTE 42", 1, "#FF0000"),
                ("42", "r42", "ROUTE 42", 1, "#FF0000"),
            ]
        elif (
            query == "SELECT DISTINCT "
            '"route_id","route_short_name","route_long_name",'
            '"route_type","route_color" '
            'FROM "routes" '
            "WHERE \"route_id\"='42'"
        ):
            return [
                ("42", "r42", "ROUTE 42", 1, "#FF0000"),
                ("42", "r42", "ROUTE 42", 1, "#FF0000"),
            ]

        elif (
            query == "SELECT "
            '"stops"."stop_id","stops"."stop_code",'
            '"stops"."stop_name","stops"."stop_lat",'
            '"stops"."stop_lon","stops"."zone_id",'
            '"routes"."route_id","route_stops"."direction_id" '
            'FROM "routes" '
            'JOIN "route_stops" ON '
            '"routes"."route_id"="route_stops"."route_id" '
            'JOIN "stops" ON '
            '"route_stops"."stop_id"="stops"."stop_id"'
        ):
            return [
                (
                    "1_42",
                    "42",
                    "Stop 42",
                    0.0,
                    0.0,
                    "A",
                    "route_id_1",
                    0,
                ),
                (
                    "1_42",
                    "42",
                    "Stop 42",
                    0.0,
                    0.0,
                    "A",
                    "route_id_2",
                    1,
                ),
                (
                    "1_43",
                    "43",
                    "Stop 43",
                    0.0,
                    0.0,
                    "B",
                    "route_id_2",
                    1,
                ),
            ]
        elif (
            query == "SELECT "
            '"stops"."stop_id","stops"."stop_code",'
            '"stops"."stop_name","stops"."stop_lat",'
            '"stops"."stop_lon","stops"."zone_id",'
            '"routes"."route_id","route_stops"."direction_id" '
            'FROM "routes" '
            'JOIN "route_stops" ON '
            '"routes"."route_id"="route_stops"."route_id" '
            'JOIN "stops" ON '
            '"route_stops"."stop_id"="stops"."stop_id" '
            'WHERE "stops"."stop_id"=\'1_42\''
        ):
            return [
                (
                    "1_42",
                    "42",
                    "Stop 42",
                    0.0,
                    0.0,
                    "A",
                    "route_id_1",
                    0,
                ),
                (
                    "1_42",
                    "42",
                    "Stop 42",
                    0.0,
                    0.0,
                    "A",
                    "route_id_2",
                    1,
                ),
            ]
        else:
            raise NotImplementedError
