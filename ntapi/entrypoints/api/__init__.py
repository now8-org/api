"""Module to store the HTTP REST API."""

from dataclasses import asdict
from typing import Dict

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from ntapi import Stop
from ntapi.logic import get_estimations

api = FastAPI(default_response_class=ORJSONResponse)

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
async def get_estimations_api(city_name: str, stop_dict: Stop = Depends(Stop)):
    """Return ETA for the next vehicles to the stop.

    Arguments:
        city_name: City name.
        stop_dict: Stop information.
    """
    try:
        result = await get_estimations(
            city_name=city_name, stop_dict=asdict(stop_dict)
        )
    except NotImplementedError:
        raise HTTPException(
            404, "Can't get estimations for the given stop in the given city."
        ) from NotImplementedError

    return result
