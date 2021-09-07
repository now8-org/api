"""Module to store the common objects for the logic layer."""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Type

from ntapi import City, CityNameError, Stop, VehicleEstimation
from ntapi.data.cities.madrid import MadridCity, MadridStop
from pydantic import validate_arguments


class Cities(str, Enum):
    """Enum with the available cities."""

    MADRID = "madrid"


# type aliases

CitiesStops = Dict[Cities, Tuple[Type[City], Type[Stop]]]

# default values

CITIES_STOPS: CitiesStops = {Cities.MADRID: (MadridCity, MadridStop)}


@validate_arguments
def assign_city_stop(
    city: str,
    cities_stops: Optional[CitiesStops] = None,
) -> Tuple[Type[City], Type[Stop]]:
    """Assign City and Stop objects corresponding to a city name.

    Arguments:
        city: Name of the city. Casing is not relevant.

    Returns:
        Corresponding City and Stop objects.

    Raises:
        CityNameError: If an invalid city name is passed.
    """
    if cities_stops is None:
        cities_stops = CITIES_STOPS

    try:
        return cities_stops[Cities(city.lower())]
    except ValueError:
        raise CityNameError(city) from ValueError


async def get_estimations(
    city_name: str, stop_dict: dict
) -> List[VehicleEstimation]:
    """Return ETA for the next vehicles to the stop.

    `stop` will be used to instantiate a Stop subclass of the given
    city.

    Arguments:
        city_name: City name.
        stop_dict: Dictionary containing the Stop information. At least
            `id_api` or `id_user` must be specified. For some
            cities, `transport_type` is also needed.

    Returns:
        ETA for the next vehicles to the stop.
    """
    city_class, stop_class = assign_city_stop(city_name)

    city = city_class()
    stop = stop_class(**stop_dict)

    return await city.get_estimations(stop)
