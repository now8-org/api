"""Module to store the main service functions."""

from abc import ABC
from enum import Enum
from os import environ
from typing import Any, Dict, List

from now8_api.data.database import SqlEngine
from now8_api.data.database.postgres import PostgresqlSqlEngine
from now8_api.service.city_data import CityData
from now8_api.service.city_data.madrid import MadridCityData
from pydantic import BaseModel


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


class Service(BaseModel, ABC):
    """Service base class.

    Attributes:
        sql_engine: SqlEngine instance for the city.
    """

    sql_engine: SqlEngine = PostgresqlSqlEngine()


def exclude(
    dict_of_dicts: Dict[Any, Dict[str, Any]], keys_to_exclude: List[str]
) -> Dict[Any, Dict[str, Any]]:
    """Filter out keys of nested dictionaries (second level).

    Arguments:
        dict_of_dicts: Nested dictionaries.
        keys_to_exclude: List with the keys to exclude.

    Returns:
        Original nested dictionary except the entries with a key in
            `keys_to_exclude` of the second level of dictionaries.
    """
    if keys_to_exclude is not None:
        return {
            key: dict(
                filter(
                    lambda key_value: key_value[0] not in keys_to_exclude,
                    value.items(),
                )
            )
            for key, value in dict_of_dicts.items()
        }

    return dict_of_dicts
