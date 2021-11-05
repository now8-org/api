"""Module to store the common objects for the entrypoints."""

from enum import Enum
from typing import Dict

from now8_api.data.database.postgres import PostgresqlSqlEngine
from now8_api.service.city_data.madrid import MadridCityData
from now8_api.service.service import Service


class Cities(str, Enum):
    """Enum with the available cities."""

    MADRID = "madrid"


CITY_SERVICES: Dict[Cities, Service] = {
    Cities.MADRID: Service(
        city_name="madrid",
        city_data=MadridCityData(),
        sql_engine=PostgresqlSqlEngine(env_prefix="MADRID_DB_"),
    )
}
