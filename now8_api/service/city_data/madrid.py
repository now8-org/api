"""Module to store the city data of Madrid."""

from json.decoder import JSONDecodeError
from typing import List, Tuple

from overrides import overrides

from now8_api.domain import (
    Estimation,
    Route,
    Stop,
    TransportType,
    Vehicle,
    VehicleEstimation,
    Way,
)
from now8_api.service.city_data import CityData, UpstreamError, get_json

CITY_NAME: str = "Madrid"


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
        except JSONDecodeError as error:
            raise UpstreamError(
                "Upstream error. Check the stop id or try later."
            ) from error

        result: List[VehicleEstimation] = []

        _estimations = response["stopTimes"]["times"].get("Time", [])
        estimations: List[dict] = (
            _estimations if isinstance(_estimations, list) else [_estimations]
        )

        for e in estimations:
            vehicle = Vehicle(
                id=e["codIssue"] if e["codIssue"] != "" else None,
                route_id=e["line"]["codLine"],
                route_way=Way(e["direction"])
                if e["direction"] in [0, 1]
                else None,
                destination_stop=Stop(
                    id=e["destinationStop"]["codStop"],
                    code=e["destinationStop"]["shortCodStop"],
                    name=e["destinationStop"]["name"],
                )
                if "codStop" in e["destinationStop"]
                and e["destinationStop"]["codStop"]
                else None,
            )
            estimation = Estimation(
                estimation=e["time"],
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
    async def get_stops_route(
        self,
        route: Route,
    ) -> Tuple[List[Stop], List[Stop]]:
        raise NotImplementedError

    @overrides
    async def get_routes_stop(
        self,
        stop: Stop,
    ) -> List[Route]:
        raise NotImplementedError
