from typing import Dict, List, Union

from fastapi import APIRouter, HTTPException
from now8_api.entrypoints.api.dependencies import Exclude, StopId
from now8_api.service.city_data import UpstreamError
from now8_api.service.service import Service

router = APIRouter(
    prefix="/stop",
    tags=["stop"],
)

service: Service = Service()


@router.get(
    "",
    summary="Get all stops in the city.",
)
async def stop_api(
    exclude: List[str] = Exclude,
) -> Dict[str, Dict[str, Union[str, float, dict]]]:
    """DO NOT CALL THIS ENDPOINT FROM THE SWAGGER UI.

    It will return a list with thousands of stop information dictionaries
    that can freeze Swagger UI. You can call the endpoint directly (without
    `/docs` in the path) with a web browser or cURL for example.
    """

    result = await service.all_stops(exclude=exclude)

    return result


@router.get(
    "/{stop_id}/info",
    summary="Get stop information.",
)
async def stop_info_api(
    stop_id: str = StopId,
) -> Dict[str, Union[str, float]]:
    try:
        result = await service.stop_info(stop_id=stop_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error

    return result


@router.get(
    "/{stop_id}/estimation",
    summary="ETA for the next vehicles to the stop.",
)
async def stop_estimation_api(
    stop_id: str = StopId,
) -> List[Dict[str, dict]]:
    try:
        result = await service.stop_estimation(stop_id=stop_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error
    except UpstreamError as error:
        raise HTTPException(
            503,
            "Upstream city API failure. Check the stop id or try again later.",
        ) from error

    return result
