"""Module to store the endpoint parameter dependencies."""

from fastapi import Path

CityName = Path(
    "madrid",
    title="City name",
    examples={"madrid": {"summary": "Madrid", "value": "madrid"}},
)
StopId = Path(
    "17491",
    title="Stop code",
    examples={
        "17491": {
            "summary": "RONDA SUR-HOSPITAL DEL SURESTE",
            "value": "17491",
        }
    },
)
