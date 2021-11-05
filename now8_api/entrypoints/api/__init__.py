"""Module to store the HTTP REST API."""

from os import environ
from typing import Dict

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from now8_api.entrypoints.common import CITY_SERVICES, Cities

description = "Estimated time of arrival for public transport vehicles."

api = FastAPI(
    name="now8 API",
    description=description,
    root_path=environ.get("ROOT_PATH", ""),
)

# internal functions


def _return_msg(msg: str, key: str = "msg") -> Dict[str, str]:
    """Return a dictionary with the provided string.

    As the value of the provided key.

    Arguments:
        msg: Message to wrap with the dictionary.
        key: Dictionary key to store the `msg` at.

    Returns:
        Resulting dictionary: `{key: msg}`.
    """
    return {key: msg}


# ROUTES


@api.get("/{city_name}/get_estimations")
async def get_estimations_api(
    city_name: Cities = Cities.MADRID, stop_id: str = "17491"
):
    """Return ETA for the next vehicles to the stop.

    - **city_name**: City name.
    - **stop_id**: Stop identifier.
    """
    try:
        result = await CITY_SERVICES.get(
            Cities(city_name.lower())
        ).get_estimations(stop_id=stop_id)
    except NotImplementedError as error:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from error

    return result
