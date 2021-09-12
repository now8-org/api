"""Module to store the common classes and functions for all cities."""

from abc import ABC, abstractmethod
from typing import List, Tuple

import aiohttp
from now8_api.domain import Line, Stop, TransportType, VehicleEstimation
from pydantic import HttpUrl, validate_arguments
from tenacity import retry, stop_after_attempt


class CityData(ABC):
    """City data abstract class.

    Abstracts the city data retrieval.
    """

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
    async def get_stops_city(
        self,
        transport_types: List[TransportType] = None,
    ) -> List[Stop]:
        """Return all the stops of the selected transport types.

        Arguments:
            transport_types: Transport types to get the stops for.
                If none are passed, all of the available ones for the
                city will be included.

        Returns:
            All the stops of the selected transport types.

        Raises:
            NotImplementedError: If the method is not implemented for
                the stop transport type in this city.
        """

    @abstractmethod
    async def get_stops_line(
        self,
        line: Line,
    ) -> Tuple[List[Stop], List[Stop]]:
        """Return all the stops of the selected line.

        Arguments:
            line: Transport line to get the stops for.

        Returns:
            Stops of the selected line for both ways in order.

        Raises:
            NotImplementedError: If the method is not implemented for
                the line transport type in this city.
        """

    @abstractmethod
    async def get_lines_stop(
        self,
        stop: Stop,
    ) -> List[Line]:
        """Return all the lines that pass through the stop.

        Arguments:
            stop: Transport stop to get the lines for.

        Returns:
            Lines that pass through the stop.

        Raises:
            NotImplementedError: If the method is not implemented for
                the stop transport type in this city.
        """


@retry(stop=stop_after_attempt(2))
@validate_arguments
async def get_json(url: HttpUrl) -> dict:
    """Fetch the given URL and returns the result as a dictionary.

     Arguments:
        url: URL to fetch.

    Returns:
        List of dictionaries with the parsed answer.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, raise_for_status=True, timeout=60) as resp:
            return await resp.json(content_type=None)
