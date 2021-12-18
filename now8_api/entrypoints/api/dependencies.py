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
        "par_8_17491": {
            "summary": "RONDA SUR-HOSPITAL DEL SURESTE (17491)",
            "value": "par_8_17491",
        },
        "par_5_11": {
            "summary": "ATOCHA (Cercanías)",
            "value": "par_5_11",
        },
        "par_6_4285": {
            "summary": "Paraninfo-Telecomunicaciones (4285)",
            "value": "par_6_4285",
        },
    },
)

RouteId = Path(
    "8__633___",
    title="Route ID",
    examples={
        "8__633___": {
            "summary": "MAJADAHONDA (Hospital)-TORRELODONES (Colonia)"
            "-GALAPAGAR-COLMENAREJO (633)",
            "value": "8__633___",
        },
        "6_N_20___": {
            "summary": "CIBELES-PITIS (N20)",
            "value": "6_N_20___",
        },
        "5__C1___": {
            "summary": "P.Pío-Atocha-Recoletos-Chamartín-Aeropuerto T4 (C1)",
            "value": "5__C1___",
        },
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
