import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from now8_api.entrypoints.api.dependencies import StopId
from now8_api.service.city_data import UpstreamError
from now8_api.service.stop_service import StopService
from pydantic import BaseModel, parse_obj_as

router = APIRouter(
    prefix="/stop",
    tags=["stop"],
)

# MODELS


class RouteWay(BaseModel):
    id: str
    way: Optional[int] = None


class StopInfo(BaseModel):
    id: str
    code: str
    name: str
    longitude: float
    latitude: float
    route_ways: List[RouteWay]
    zone: Optional[str] = None


StopInfos = Dict[str, StopInfo]


class Vehicle(BaseModel):
    id: str
    route_way: RouteWay = None
    name: Optional[str] = None


class Estimation(BaseModel):
    time: datetime.datetime
    estimation: datetime.datetime


class VehicleEstimation(BaseModel):
    vehicle: Vehicle
    estimation: Estimation


StopEstimations = List[VehicleEstimation]

# ROUTES

stop_service: StopService = StopService()


@router.get("", summary="Get all stops in the city.", response_model=StopInfos)
async def stop_api() -> StopInfos:
    """DO NOT CALL THIS ENDPOINT FROM THE SWAGGER UI.

    It will return a list with thousands of stop information dictionaries
    that can freeze Swagger UI. You can call the endpoint directly (without
    `/docs` in the path) with a web browser or cURL for example.
    """

    result = parse_obj_as(
        StopInfos,
        await stop_service.all_stops(),
    )

    return result


@router.get(
    "/{stop_id}/info", summary="Get stop information.", response_model=StopInfo
)
async def stop_info_api(
    stop_id: str = StopId,
) -> StopInfo:
    try:
        result = StopInfo.parse_obj(
            await stop_service.stop_info(stop_id=stop_id)
        )
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error

    return result


@router.get(
    "/{stop_id}/estimation",
    summary="ETA for the next vehicles to the stop.",
    response_model=StopEstimations,
)
async def stop_estimation_api(
    stop_id: str = StopId,
) -> StopEstimations:
    try:
        result = parse_obj_as(
            StopEstimations,
            await stop_service.stop_estimation(stop_id=stop_id),
        )
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
