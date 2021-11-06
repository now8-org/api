from typing import Dict, List, Union

from fastapi import APIRouter, HTTPException
from now8_api.entrypoints.api.dependencies import CityName, StopId
from now8_api.entrypoints.common import CITY_SERVICES, Cities
from now8_api.service.service import Service

router = APIRouter(
    prefix="/stop",
    tags=["stop"],
)


@router.get(
    "/{city_name}/{stop_id}",
    summary="Get all stops in a city.",
)
async def stop_api(
    city_name: str = CityName,
    stop_id: str = StopId,
) -> List[Dict[str, str]]:
    return []


@router.get(
    "/{city_name}/{stop_id}/info",
    summary="Get stop information.",
)
async def stop_info_api(
    city_name: str = CityName,
    stop_id: str = StopId,
) -> Dict[str, Union[str, float]]:
    try:
        city_service: Service = CITY_SERVICES.get(Cities(city_name.lower()))
    except KeyError as error:
        raise HTTPException(400, f'Invalid city name "{city_name}"') from error

    try:
        result = await city_service.stop_info(stop_id=stop_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error

    return result


@router.get(
    "/{city_name}/{stop_id}/estimation",
    summary="ETA for the next vehicles to the stop.",
)
async def stop_estimation_api(
    city_name: str = CityName,
    stop_id: str = StopId,
) -> List[Dict[str, dict]]:
    try:
        city_service: Service = CITY_SERVICES.get(Cities(city_name.lower()))
    except KeyError as error:
        raise HTTPException(400, f'Invalid city name "{city_name}"') from error

    try:
        result = await city_service.stop_estimation(stop_id=stop_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error

    return result
