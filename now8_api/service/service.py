"""Module to store the main service functions."""

from enum import Enum
from os import environ
from typing import Any, Dict, List, Union

from now8_api.data.database import SqlEngine
from now8_api.data.database.postgres import PostgresqlSqlEngine
from now8_api.domain import Coordinates, Stop, TransportType
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData
from pydantic import BaseModel
from pypika import Query, Table


class Cities(str, Enum):
    """Enum with the available cities."""

    MADRID = "madrid"


try:
    CITY: Cities = Cities(environ.get("CITY", "madrid").lower())
except ValueError as error:
    raise ValueError(
        f"Invalid CITY environment variable value. "
        f"Must be one of {[city.value for city in Cities]}."
    ) from error

CITY_DATA_DICT: Dict[Cities, CityData] = {
    Cities.MADRID: MadridCityData(),
}


class Service(BaseModel):
    """Service base class.

    Attributes:
        city_data: CityData instance for the city.
        sql_engine: SqlEngine instance for the city.
        stops_cache: Object to store the stops info.
    """

    city_data: CityData = CITY_DATA_DICT[CITY]
    sql_engine: SqlEngine = PostgresqlSqlEngine()

    stops_cache: Dict[str, Dict[str, Any]] = None

    async def initialize_stops_cache(self) -> None:
        """Initialize `stops_cache` if undefined."""
        table_stops: Table = Table("stops")
        query: Query = Query.from_(table_stops).select(
            table_stops.stop_id,
            table_stops.stop_code,
            table_stops.stop_name,
            table_stops.stop_lat,
            table_stops.stop_lon,
            table_stops.zone_id,
        )
        query_result: List[tuple] = await self.sql_engine.execute_query(
            str(query)
        )

        result: Dict[str, Dict[str, Union[str, float, dict]]] = {}
        for row in query_result:
            stop = Stop(
                id=row[0],
                code=row[1],
                name=row[2],
                coordinates=Coordinates(latitude=row[3], longitude=row[4]),
                zone=row[5],
            )

            result[stop.id] = {
                "code": stop.code,
                "name": stop.name,
                "longitude": stop.coordinates.longitude,
                "latitude": stop.coordinates.latitude,
                "zone": stop.zone,
                "lines": {},
            }

        self.stops_cache = result

    async def all_stops(
        self, exclude: List[str] = None
    ) -> Dict[str, Dict[str, Union[str, float, dict]]]:
        """Return all the stops of the city.

        Returns:
            List of dictionaries with the stop ID, transport type, way,
            name, coordinates and zone of each stop.
        """
        if self.stops_cache is None:
            await self.initialize_stops_cache()

        if exclude is not None:
            return {
                key: dict(
                    filter(
                        lambda key_value: key_value[0] not in exclude,
                        value.items(),
                    )
                )
                for key, value in self.stops_cache.items()
            }
        else:
            return self.stops_cache

    async def stop_info(self, stop_id: str) -> Dict[str, Union[str, float]]:
        """Return the stop information.

        Arguments:
            stop_id: Stop identifier.

        Returns:
            Dictionary with the stop ID, transport type, way, name,
                coordinates and zone.

        Raises:
            ValueError: If the `stop_id` does not match any stop.
        """
        if self.stops_cache is None:
            await self.initialize_stops_cache()

        return self.stops_cache[stop_id]

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
                    "line": {
                        "id": v_e.vehicle.line.id,
                        "transport_type": v_e.vehicle.line.transport_type.value,  # noqa: E501
                        "name": v_e.vehicle.line.name,
                    },
                    "name": v_e.vehicle.name,
                },
                "estimation": {
                    "estimation": v_e.estimation.estimation,
                    "time": v_e.estimation.time,
                },
            }
            for v_e in estimations
        ]

        return result
