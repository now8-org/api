"""Module to store the endpoint parameter dependencies."""

from typing import List

from fastapi import Path, Query

CityName = Path(
    "madrid",
    title="City name",
    examples={"madrid": {"summary": "Madrid", "value": "madrid"}},
)

StopId = Path(
    "17491",
    title="Stop code",
    examples={
        "coordinates and lines": {
            "summary": "Exclude coordinates and lines.",
            "value": ["longitude", "latitude", "lines"],
        }
    },
)

Exclude: List[str] = Query(
    [],
    title="Stop attributes to exclude.",
    examples={
        "17491": {
            "summary": "RONDA SUR-HOSPITAL DEL SURESTE",
            "value": "17491",
        }
    },
)
