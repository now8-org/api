"""Module to store the endpoint parameter dependencies."""

from fastapi import Path, Query

CityName = Path(
    "madrid",
    title="City name",
    examples={"madrid": {"summary": "Madrid", "value": "madrid"}},
)

StopId = Path(
    "par_8_17491",
    title="Stop ID",
    examples={
        "17491": {
            "summary": "RONDA SUR-HOSPITAL DEL SURESTE (17491)",
            "value": "par_8_17491",
        }
    },
)

RouteId = Path(
    "633",
    title="Route ID",
    examples={
        "633": {
            "summary": "MADRID (Plaza de Castilla) - ALCOBENDAS (151)",
            "value": "633",
        }
    },
)

Exclude = Query(
    None,
    title="Stop attributes to exclude.",
    examples={
        "id and name": {
            "summary": "Exclude name and id.",
            "value": ["name", "id"],
        }
    },
)
