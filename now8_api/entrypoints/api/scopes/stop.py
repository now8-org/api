from typing import Dict, List, Union

from fastapi import APIRouter, HTTPException
from now8_api.entrypoints.api.dependencies import StopId
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
async def stop_api() -> List[Dict[str, Union[str, float]]]:

    result = await service.all_stops()

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

    return result
