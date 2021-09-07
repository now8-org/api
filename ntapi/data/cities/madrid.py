"""Module to store the City of Madrid."""

from typing import Dict, List

from ntapi import (
    City,
    Estimation,
    Line,
    Stop,
    TransportType,
    TransportTypeError,
    Vehicle,
    VehicleEstimation,
)
from ntapi.data.cities import get_json
from overrides import overrides
from pydantic import root_validator
from pydantic.dataclasses import dataclass

TRANSPORT_TYPE_STOP_PREFIXES: Dict[TransportType, str] = {
    TransportType.INTERCITY_BUS: "8_"
}


class MadridCity(City):
    """Madrid city."""

    name: str = "Madrid"
    transport_types: List[TransportType] = list(
        TRANSPORT_TYPE_STOP_PREFIXES.keys()
    )

    @overrides
    async def get_estimations(
        self,
        stop: Stop,
    ) -> List[VehicleEstimation]:
        if stop.transport_type == TransportType.INTERCITY_BUS:
            response = await get_json(
                f"https://www.crtm.es/"  # type: ignore
                f"widgets/api/GetStopsTimes.php"
                f"?codStop={stop.id_api}&type=1&orderBy=2&stopTimesByIti=3"
            )
        else:
            raise NotImplementedError

        result: List[VehicleEstimation] = []

        for estimation in response["stopTimes"]["times"]["Time"]:
            line = Line(
                id_api=estimation["line"]["codLine"],
                id_user=estimation["line"]["shortDescription"],
                transport_type=TransportType.INTERCITY_BUS,
                name=estimation["line"]["description"],
            )
            vehicle = Vehicle(line=line, identifier=estimation["codIssue"])
            estimation = Estimation(
                estimation=estimation["time"],
                time=response["stopTimes"]["actualDate"],
            )
            result.append(
                VehicleEstimation(vehicle=vehicle, estimation=estimation)
            )

        return result

    async def get_stops(
        self,
        transport_types: List[TransportType] = None,
    ) -> List[Stop]:
        """Return all the stops of the selected transport types."""
        raise NotImplementedError


@dataclass
class MadridStop(Stop):
    """Transportation stop."""

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
        elif values["id_api"] is None:
            try:
                values["id_api"] = (
                    TRANSPORT_TYPE_STOP_PREFIXES[values["transport_type"]]
                    + values["id_user"]
                )
            except KeyError:
                raise TransportTypeError(
                    values["transport_type"], MadridCity()
                ) from KeyError
        elif values["id_user"] is None:
            try:
                values["id_user"] = values["id_api"].removeprefix(
                    TRANSPORT_TYPE_STOP_PREFIXES[values["transport_type"]]
                )
            except KeyError:
                raise TransportTypeError(
                    values["transport_type"], MadridCity()
                ) from KeyError

        return values
