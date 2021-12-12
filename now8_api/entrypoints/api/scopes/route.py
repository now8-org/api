from typing import Dict, List, Union

from fastapi import APIRouter, HTTPException
from now8_api.entrypoints.api.dependencies import Exclude, RouteId
from now8_api.service.route_service import RouteService

router = APIRouter(
    prefix="/route",
    tags=["route"],
)

service: RouteService = RouteService()


@router.get(
    "",
    summary="Get all routes in the city.",
)
async def route_api(
    keys_to_exclude: List[str] = Exclude,
) -> Dict[str, Dict[str, Union[str, float, dict]]]:
    """DO NOT CALL THIS ENDPOINT FROM THE SWAGGER UI.

    It will return a list with thousands of route information dictionaries
    that can freeze Swagger UI. You can call the endpoint directly (without
    `/docs` in the path) with a web browser or cURL for example.
    """

    result = await service.all_routes(keys_to_exclude=keys_to_exclude)

    return result


@router.get(
    "/{route_id}/info",
    summary="Get route information.",
)
async def route_info_api(
    route_id: str = RouteId,
) -> Dict[str, Union[str, float]]:
    try:
        result = await service.route_info(route_id=route_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given route in the given city."
        ) from error

    return result
