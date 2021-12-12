"""Module to store the city data of Madrid."""

from typing import Dict, List, Tuple

from now8_api.domain import (
    Estimation,
    Route,
    Stop,
    TransportType,
    Vehicle,
    VehicleEstimation,
)
from now8_api.service import TransportTypeError
from now8_api.service.city_data import CityData, UpstreamError, get_json
from overrides import overrides

CITY_NAME: str = "Madrid"

TRANSPORT_TYPE_STOP_PREFIXES: Dict[TransportType, str] = {
    TransportType.INTERCITY_BUS: "8_"
}


def _stop_id_user(stop_id_api: str, transport_type: TransportType) -> str:
    """Return the Stop ID in the user format.

    Arguments:
        stop_id_api: Stop ID in the city API format.
        transport_type: Stop transport type.

    Returns:
        Stop ID in the user format.

    Raises:
        TransportTypeError: If the transport type is not
            supported.
    """
    if transport_type not in TRANSPORT_TYPE_STOP_PREFIXES:
        raise TransportTypeError(transport_type=transport_type.name)

    return stop_id_api.removeprefix(
        TRANSPORT_TYPE_STOP_PREFIXES[transport_type]
    )


def _stop_id_api(stop_id_user: str, transport_type: TransportType) -> str:
    """Return the Stop ID in the API format.

    Arguments:
        stop_id_user: Stop ID in the user format.
        transport_type: Stop transport type.

    Returns:
        Stop ID in the API format.

    Raises:
        TransportTypeError: If the transport type is not
            supported.
    """
    if transport_type not in TRANSPORT_TYPE_STOP_PREFIXES:
        raise TransportTypeError(transport_type=transport_type.name)

    return TRANSPORT_TYPE_STOP_PREFIXES[transport_type] + stop_id_user


class MadridCityData(CityData):
    """Madrid city data."""

    @overrides
    async def get_estimations(
        self,
        stop: Stop,
    ) -> List[VehicleEstimation]:
        try:
            response = await get_json(
                f"https://www.crtm.es/"  # type: ignore
                f"widgets/api/GetStopsTimes.php"
                f"?codStop="
                f"{stop.id.removeprefix('par_').removeprefix('est_')}&"
                f"type=1&orderBy=2&stopTimesByIti=3"
            )
        except Exception as error:
            raise UpstreamError(
                "Upstream error. Check the stop id or try later."
            ) from error

        result: List[VehicleEstimation] = []

        for estimation in response["stopTimes"]["times"].get("Time", []):
            line = Route(
                id=estimation["line"]["codLine"],
                code=estimation["line"]["shortDescription"],
                transport_type=TransportType(
                    int(estimation["line"]["codMode"])
                ),
                name=estimation["line"]["description"],
            )
            vehicle = Vehicle(line=line, id=estimation["codIssue"])
            estimation = Estimation(
                estimation=estimation["time"],
                time=response["stopTimes"]["actualDate"],
            )
            result.append(
                VehicleEstimation(vehicle=vehicle, estimation=estimation)
            )

        return result

    @overrides
    async def get_stops_city(
        self,
        transport_types: List[TransportType] = None,
    ) -> List[Stop]:
        raise NotImplementedError

    @overrides
    async def get_stops_line(
        self,
        line: Route,
    ) -> Tuple[List[Stop], List[Stop]]:
        raise NotImplementedError

    @overrides
    async def get_lines_stop(
        self,
        stop: Stop,
    ) -> List[Route]:
        raise NotImplementedError
