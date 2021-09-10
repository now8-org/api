"""Module to store the common classes and exceptions."""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, TypedDict

from pydantic import BaseModel, root_validator, validator
from pydantic.dataclasses import dataclass


class TransportType(Enum):
    """Transport type (bus, metro, train, etc.)."""

    BUS = "bus"
    INTERCITY_BUS = "intercity_bus"
    NIGHT_BUS = "Night_bus"
    METRO = "METRO"
    CITRY_TRAIN = "city_train"
    TRAM = "TRAM"


class Way(Enum):
    """Way (inbound or outbound)."""

    OUTBOUND = 0
    INBOUND = 1


@dataclass
class Line:
    """Transport line.

    Attributes:
        id_api: Line identifier in the API format.
        id_user: Line identifier in the user format.
        transport_type: Transport type of the line.
        name: Line name.
    """

    id_api: Optional[str] = None
    id_user: Optional[str] = None
    transport_type: Optional[TransportType] = None
    name: Optional[str] = None

    @root_validator
    @classmethod
    def default_ids(cls, values):
        """Set the default value for the id_api or id_user if unspecified.

        Raises:
            ValueError: If neither `id_api` nor `id_user` are defined.
        """
        if values["id_api"] is None and values["id_user"] is None:
            raise ValueError(
                "At least `id_api` or `id_user` have to be specified."
            )

        if values["id_api"] is None:
            values["id_api"] = values["id_user"]
        elif values["id_user"] is None:
            values["id_user"] = values["id_api"]

        return values

    @validator("name", always=True)
    @classmethod
    def default_name(cls, value, values):
        """Set the default value for the name if unspecified."""
        if value is None:
            value = values["id_user"]
        return value


@dataclass
class Vehicle:
    """Transport vehicle.

    Attributes:
        identifier: Vehicle identifier.
        line: Line to which the vehicle belongs to.
        name: Vehicle name.
    """

    identifier: str
    line: Line
    name: Optional[str] = None

    @validator("name", pre=True, always=True)
    @classmethod
    def default_name(cls, value, values):
        """Set the default value for the name if unspecified."""
        if value is None:
            value = values["identifier"]
        return value


@dataclass
class Estimation:
    """Estimation class.

    Attributes:
        estimation: Estimated time of arrival.
        time: Time when the estimation was made.
    """

    estimation: datetime
    time: Optional[datetime] = None

    @validator("time")
    @classmethod
    def set_time(cls, value):
        """Set time to current time if not specified."""
        if value is None:
            value = datetime.now()
        return value


class VehicleEstimation(TypedDict):
    """Vehicle estimated time of arrival.

    Attributes:
        vehicle: Vehicle for which the estimation is for.
        estimation: Estimated time of arrival.
    """

    vehicle: Vehicle
    estimation: Estimation


@dataclass
class Stop(ABC):
    """Transportation stop.

    Attributes:
        id_user: Stop identifier in the user format.
        id_api: Stop identifier in the API format.
        transport_type: Transport type of the stop.
        way: Way of the stop.
        name: Name of the stop.
        coordinates: Coordinates where the stop is located at.
    """

    id_user: Optional[str] = None
    id_api: Optional[str] = None
    transport_type: Optional[TransportType] = None
    way: Optional[Way] = None
    name: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None

    # See bug https://github.com/samuelcolvin/pydantic/issues/1973
    # @root_validator
    # @classmethod
    # def default_ids(cls, values):
    #    """Set the default value for the id_api or id_user if unspecified.

    #    Raises:
    #        ValueError: If neither `id_api` nor `id_user` are defined.
    #    """


class City(BaseModel, ABC):
    """City.

    Attributes:
        name: City name.
        transport_types: Supported transport types for the city.
    """

    name: str = ""
    transport_types: List[TransportType] = []

    @abstractmethod
    async def get_estimations(
        self,
        stop: Stop,
    ) -> List[VehicleEstimation]:
        """Return ETA for the next vehicles to the stop.

        Arguments:
            stop: Stop to get the next vehicle arrival estimations for.

        Returns:
            ETA for the next vehicles to the stop.

        Raises:
            NotImplementedError: If the method is not implemented for
                the stop transport type in this city.
        """

    @abstractmethod
    async def get_stops(
        self,
        transport_types: List[TransportType] = None,
    ) -> List[Stop]:
        """Return all the stops of the selected transport types."""


# ERRORS


class TransportTypeError(ValueError):
    """Invalid transport type error."""

    def __init__(self, transport_type: str, city: City):
        """Set the error message and raise the exception.

        Arguments:
            transport_type: Invalid transport type passed.
            city: City for which the transport type is invalid.
        """
        message = (
            f"Invalid transport type '{transport_type}' for city "
            f"'{city.name}'."
        )
        super().__init__(message)


class StopIdError(ValueError):
    """Invalid stop ID error."""

    def __init__(self, stop_id: str):
        """Set the error message and raise the exception.

        Arguments:
            stop_id: Invalid stop identifier passed.
        """
        message = f"Invalid stop ID '{stop_id}'."
        super().__init__(message)


class CityNameError(ValueError):
    """Invalid city name error."""

    def __init__(self, city: str):
        """Set the error message and raise the exception.

        Arguments:
            city: Invalid city name passed.
        """
        message = f"Invalid city name '{city}'."
        super().__init__(message)
