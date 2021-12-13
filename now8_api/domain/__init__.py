"""Module to store the common domain objects."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field
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
    FUNICULAR = 7
    INTERCITY_BUS = 8
    URBAN_BUS = 9
    TROLLEY_BUS = 11
    MONORAIL = 12


class Way(int, Enum):
    """Way (inbound or outbound)."""

    OUTBOUND = 0
    INBOUND = 1


@dataclass
class Route:
    """Transport route.

    Attributes:
        id: Route identifier.
        code: Route identifier in the user format.
        transport_type: Transport type of the route.
        name: Route name.
        color: Route color.
    """

    id: str
    code: str = None
    transport_type: Optional[TransportType] = None
    name: Optional[str] = None
    color: Color = None


@dataclass
class Vehicle:
    """Transport vehicle.

    Attributes:
        id: Vehicle identifier.
        route_id: Route to which the vehicle belongs to.
        name: Vehicle name.
    """

    id: str
    route_id: str
    route_way: Optional[Way] = None
    name: Optional[str] = None


@dataclass
class Estimation:
    """Estimation class.

    Attributes:
        estimation: Estimated time of arrival.
        time: Time when the estimation was made.
    """

    time: datetime
    estimation: datetime


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
        name: Name of the stop.
        transport_type: Transport type of the stop.
        coordinates: Coordinates where the stop is located at.
        zone: Zone where the stop is located at.
    """

    id: str
    code: Optional[str] = None
    name: Optional[str] = None
    transport_type: Optional[TransportType] = None
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
