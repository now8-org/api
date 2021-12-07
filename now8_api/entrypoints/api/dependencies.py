"""Module to store the endpoint parameter dependencies."""

from fastapi import Path, Query

CityName = Path(
    "madrid",
    title="City name",
    examples={"madrid": {"summary": "Madrid", "value": "madrid"}},
)

StopId = Path(
    "par_8_17491",
    title="Stop code",
    examples={
        "17491": {
            "summary": "RONDA SUR-HOSPITAL DEL SURESTE (17491)",
            "value": "par_8_17491",
        }
    },
)

Exclude = Query(
    None,
    title="Stop attributes to exclude.",
    examples={
        "coordinates and lines": {
            "summary": "Exclude coordinates and lines.",
            "value": ["longitude", "latitude", "lines"],
        }
    },
)
