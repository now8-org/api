"""Module to store the main service functions."""

from enum import Enum
from typing import Dict, List

from now8_api.domain import Stop, TransportType
from now8_api.service import CityNameError
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData


class Cities(str, Enum):
    """Enum with the available cities."""

    MADRID = "madrid"


CITIES_CITY_DATA: Dict[Cities, CityData] = {Cities.MADRID: MadridCityData()}


def _assign_city_data(
    city_name: str,
) -> CityData:
    """Assign CityData instance corresponding to a city name.

    Arguments:
        city_name: Name of the city. Casing is not relevant.

    Returns:
        Corresponding CityData instance.

    Raises:
        CityNameError: If an invalid city name is passed.
    """
    try:
        city = Cities(city_name.lower())
    except ValueError as error:
        raise CityNameError(city_name=city_name) from error

    return CITIES_CITY_DATA[city]


async def get_estimations(
    city_name: str, stop_id: str
) -> List[Dict[str, dict]]:
    """Return ETA for the next vehicles to the stop.

    `stop` will be used to instantiate a Stop subclass of the given
    city.

    Arguments:
        city_name: City name.
        stop_id: Stop identifier.

    Returns:
        ETA for the next vehicles to the stop.
    """
    city_data = _assign_city_data(city_name)

    stop = Stop(id=stop_id, transport_type=TransportType.INTERCITY_BUS)

    estimations = await city_data.get_estimations(stop)

    result: List[Dict[str, dict]] = [
        {
            "vehicle": {
                "id": v_e.vehicle.id,
                "line": {
                    "id": v_e.vehicle.line.id,
                    "transport_type": v_e.vehicle.line.transport_type.value,
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
