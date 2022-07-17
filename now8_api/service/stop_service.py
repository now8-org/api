from typing import Any, Dict, List, Union

from pypika import Query, Table

from now8_api.domain import Coordinates, Stop, TransportType
from now8_api.service.service import CITY, CITY_DATA_DICT, CityData, Service


class StopNotFoundError(ValueError):
    """Custom exception for stop not found."""

    def __init__(self, stop_id: str) -> None:
        """Initialize ValueError with custom message.

        Arguments:
            stop_id: Stop ID that was not found.
        """
        super().__init__(f'Stop "{stop_id}" not found.')


_table_routes: Table = Table("routes")
_table_route_stops: Table = Table("route_stops")
_table_stops: Table = Table("stops")
_all_stops_query: Query = (
    Query.from_(_table_routes)
    .join(_table_route_stops)
    .on(_table_routes.route_id == _table_route_stops.route_id)
    .join(_table_stops)
    .on(_table_route_stops.stop_id == _table_stops.stop_id)
    .select(
        _table_stops.stop_id,
        _table_stops.stop_code,
        _table_stops.stop_name,
        _table_stops.stop_lat,
        _table_stops.stop_lon,
        _table_stops.zone_id,
        _table_routes.route_id,
        _table_route_stops.direction_id,
    )
)


class StopService(Service):
    """Service base class.

    Attributes:
        city_data: CityData instance for the city.
    """

    city_data: CityData = CITY_DATA_DICT[CITY]

    async def all_stops(
        self,
    ) -> Dict[str, Dict[str, Union[str, float, dict]]]:
        """Return all the stops of the city.

        Returns:
            List of dictionaries with the stop ID, transport type, way,
            name, coordinates and zone of each stop.
        """
        query_result: List[tuple] = await self.sql_engine.execute_query(
            str(_all_stops_query)
        )

        result: Dict[str, Dict[str, Any]] = {}
        for row in query_result:
            stop_id: str = row[0]
            stop_code: str = row[1]
            stop_name: str = row[2]
            stop_lat: float = row[3]
            stop_lon: float = row[4]
            stop_zone: str = row[5]

            if stop_id not in result:
                stop = Stop(
                    id=stop_id,
                    code=stop_code,
                    name=stop_name,
                    coordinates=Coordinates(
                        latitude=stop_lat, longitude=stop_lon
                    ),
                    zone=stop_zone,
                )

                result[stop.id] = {
                    "id": stop.id,
                    "code": stop.code,
                    "name": stop.name,
                    "longitude": stop.coordinates.longitude,
                    "latitude": stop.coordinates.latitude,
                    "zone": stop.zone,
                    "route_ways": [],
                }

            route_id: str = row[6]
            route_way: int = row[7]

            result[stop_id]["route_ways"].append(
                {"id": route_id, "way": route_way}
            )

        return result

    async def stop_info(
        self, stop_id: str
    ) -> Dict[str, Union[str, float, list]]:
        """Return the stop information.

        Arguments:
            stop_id: Stop identifier.

        Returns:
            Dictionary with the stop ID, transport type, way, name,
                coordinates and zone.

        Raises:
            StopNotFoundError: If the `stop_id` does not match any stop.
        """
        query_result: List[tuple] = await self.sql_engine.execute_query(
            str(_all_stops_query.where(_table_stops.stop_id == stop_id))
        )

        if len(query_result) < 1:
            raise StopNotFoundError(stop_id=stop_id)

        result: Dict[str, Any] = {}
        for row in query_result:
            stop_code: str = row[1]
            stop_name: str = row[2]
            stop_lat: float = row[3]
            stop_lon: float = row[4]
            stop_zone: str = row[5]

            if result == {}:
                stop = Stop(
                    id=stop_id,
                    code=stop_code,
                    name=stop_name,
                    coordinates=Coordinates(
                        latitude=stop_lat, longitude=stop_lon
                    ),
                    zone=stop_zone,
                )

                result = {
                    "id": stop.id,
                    "code": stop.code,
                    "name": stop.name,
                    "longitude": stop.coordinates.longitude,
                    "latitude": stop.coordinates.latitude,
                    "zone": stop.zone,
                    "route_ways": [],
                }

            route_id: str = row[6]
            route_way: int = row[7]

            result["route_ways"].append({"id": route_id, "way": route_way})

        return result

    async def stop_estimation(self, stop_id: str) -> List[Dict[str, dict]]:
        """Return ETA for the next vehicles to the stop.

        Arguments:
            stop_id: Stop identifier.

        Returns:
            ETA for the next vehicles to the stop.
        """
        stop = Stop(id=stop_id, transport_type=TransportType.INTERCITY_BUS)

        estimations = await self.city_data.get_estimations(stop)

        result: List[Dict[str, dict]] = [
            {
                "vehicle": {
                    "id": v_e.vehicle.id,
                    "route_way": {
                        "id": v_e.vehicle.route_id,
                        "way": v_e.vehicle.route_way.value
                        if v_e.vehicle.route_way is not None
                        else None,
                    },
                    "destination_stop": {
                        "id": v_e.vehicle.destination_stop.id,
                        "code": v_e.vehicle.destination_stop.code,
                        "name": v_e.vehicle.destination_stop.name,
                    },
                },
                "estimation": {
                    "estimation": v_e.estimation.estimation,
                    "time": v_e.estimation.time,
                },
            }
            for v_e in estimations
        ]

        return result
