from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache
from now8_api.entrypoints.api.dependencies import RouteId
from now8_api.service.route_service import RouteNotFoundError, RouteService
from pydantic import BaseModel, parse_obj_as
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter(
    prefix="/route",
    tags=["route"],
)


@router.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


# MODELS


class RouteInfo(BaseModel):
    id: str
    code: str
    name: str
    transport_type: int
    color: Optional[str] = None


RouteInfos = Dict[str, RouteInfo]

# ROUTES

service: RouteService = RouteService()


@router.get(
    "", summary="Get all routes in the city.", response_model=RouteInfos
)
@cache(expire=7 * 24 * 60 * 60, coder=PickleCoder)  # 7 days
async def route_api(
    request: Request,
    respone: Response,
):
    """DO NOT CALL THIS ENDPOINT FROM THE SWAGGER UI.

    It will return a list with thousands of route information dictionaries
    that can freeze Swagger UI. You can call the endpoint directly (without
    `/docs` in the path) with a web browser or cURL for example.
    """

    result = parse_obj_as(RouteInfos, await service.all_routes())

    return ORJSONResponse(content=jsonable_encoder(result))


@router.get(
    "/{route_id}/info",
    summary="Get route information.",
    response_model=RouteInfo,
)
@cache(expire=7 * 24 * 60 * 60, coder=PickleCoder)  # 7 days
async def route_info_api(
    route_id: str = RouteId,
):
    try:
        result = RouteInfo.parse_obj(
            await service.route_info(route_id=route_id)
        )
    except RouteNotFoundError as error:
        raise HTTPException(404, "Route not found.") from error

    return ORJSONResponse(content=jsonable_encoder(result))
