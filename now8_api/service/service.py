"""Module to store the main service functions."""

from enum import Enum
from typing import Dict, List

from now8_api.domain import Stop, TransportType, VehicleEstimation
from now8_api.service import CityNameError
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData


class Cities(str, Enum):
    """Enum with the available cities."""

    MADRID = "madrid"


CITIES_CITY_DATA: Dict[Cities, CityData] = {Cities.MADRID: MadridCityData()}


def assign_city_data(
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
) -> List[VehicleEstimation]:
    """Return ETA for the next vehicles to the stop.

    `stop` will be used to instantiate a Stop subclass of the given
    city.

    Arguments:
        city_name: City name.
        stop_id: Stop identifier.

    Returns:
        ETA for the next vehicles to the stop.
    """
    city_data = assign_city_data(city_name)

    stop = Stop(id=stop_id, transport_type=TransportType.INTERCITY_BUS)

    return await city_data.get_estimations(stop)
