"""Module to store the common domain objects."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field, validator
from pydantic.color import Color
from pydantic.dataclasses import dataclass


class TransportType(int, Enum):
    """Transport type (bus, metro, train, etc.)."""

    TRAM = 0
    METRO = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    AERIAL_LIFT = 6
    FUNICULAR = 6
    INTERCITY_BUS = 8
    TROLLEY_BUS = 11
    MONORAIL = 12


class Way(Enum):
    """Way (inbound or outbound)."""

    OUTBOUND = 0
    INBOUND = 1


@dataclass
class Line:
    """Transport line.

    Attributes:
        id: Line identifier.
        code: Line identifier in the user format.
        transport_type: Transport type of the line.
        name: Line name.
        way: Way (inbound or outbound).
        color: Line color.
    """

    id: str
    code: str = None
    transport_type: Optional[TransportType] = None
    name: Optional[str] = None
    way: Way = None
    color: Color = None


@dataclass
class Vehicle:
    """Transport vehicle.

    Attributes:
        id: Vehicle identifier.
        line: Line to which the vehicle belongs to.
        name: Vehicle name.
    """

    id: str
    line: Line
    name: Optional[str] = None

    @validator("name", pre=True, always=True)
    @classmethod
    def default_name(cls, value, values):
        """Set the default value for the name if unspecified."""
        if value is None:
            value = values["id"]
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


@dataclass
class VehicleEstimation:
    """Vehicle estimated time of arrival.

    Attributes:
        vehicle: Vehicle for which the estimation is for.
        estimation: Estimated time of arrival.
    """

    vehicle: Vehicle
    estimation: Estimation


@dataclass
class Coordinates:
    """Coordinates (in degrees).

    Attributes:
        longitude: Longitude.
        latitude: Latitude.
    """

    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)


@dataclass
class Stop:
    """Transportation stop.

    Attributes:
        id: Stop identifier.
        code: Stop identifier in the user format.
        transport_type: Transport type of the stop.
        way: Way of the stop.
        name: Name of the stop.
        coordinates: Coordinates where the stop is located at.
        zone: Zone where the stop is located at.
    """

    id: str
    code: Optional[str] = None
    transport_type: Optional[TransportType] = None
    way: Optional[Way] = None
    name: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    zone: Optional[str] = None


@dataclass
class City:
    """City.

    Attributes:
        name: City name.
        transport_types: Supported transport types for the city.
    """

    name: str = ""
    transport_types: List[TransportType] = None
