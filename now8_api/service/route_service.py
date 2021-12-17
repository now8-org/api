"""Module to store the main service functions."""

from typing import Dict, List, Union

from now8_api.domain import Route, TransportType
from now8_api.service.service import Service
from pydantic.color import Color
from pypika import Query, Table


class RouteNotFoundError(ValueError):
    """Custom exception for route not found."""

    def __init__(self, route_id: str) -> None:
        """Initialize ValueError with custom message.

        Arguments:
            route_id: Route ID that was not found.
        """
        super().__init__(f'Route "{route_id}" not found.')


class RouteService(Service):
    async def all_routes(
        self,
    ) -> Dict[str, Dict[str, Union[str, float, dict]]]:
        """Return all the routes of the city.

        Returns:
            List of dictionaries with the route ID, transport type, way,
            name, coordinates and zone of each route.
        """
        table_routes: Table = Table("routes")
        query: Query = (
            Query.from_(table_routes)
            .select(
                table_routes.route_id,
                table_routes.route_short_name,
                table_routes.route_long_name,
                table_routes.route_type,
                table_routes.route_color,
            )
            .distinct()
        )
        query_result: List[tuple] = await self.sql_engine.execute_query(
            str(query)
        )

        result: Dict[str, Dict[str, Union[str, float, dict]]] = {}
        for row in query_result:
            route_id: str = row[0]
            route_code: str = row[1]
            route_name: str = row[2]
            route_type: int = row[3]
            route_color: str = row[4]

            route = Route(
                id=route_id,
                code=route_code,
                name=route_name,
                transport_type=TransportType(route_type),
                color=Color(route_color),
            )

            result[route.id] = {
                "id": route.id,
                "code": route.code,
                "name": route.name,
                "transport_type": route.transport_type.value,
                "color": str(route.color.original()),
            }

        return result

    async def route_info(self, route_id: str) -> Dict[str, Union[str, float]]:
        """Return the route information.

        Arguments:
            route_id: Route identifier.

        Returns:
            Dictionary with the route ID, transport type, way, name,
                coordinates and zone.

        Raises:
            RouteNotFoundError: If the `route_id` does not match any route.
        """
        table_routes: Table = Table("routes")
        query: Query = (
            Query.from_(table_routes)
            .select(
                table_routes.route_id,
                table_routes.route_short_name,
                table_routes.route_long_name,
                table_routes.route_type,
                table_routes.route_color,
            )
            .where(table_routes.route_id == route_id)
            .distinct()
        )
        query_result: List[tuple] = await self.sql_engine.execute_query(
            str(query)
        )

        if len(query_result) < 1:
            raise RouteNotFoundError(route_id=route_id)

        result: Dict[str, Union[str, float]] = {}

        row = query_result[0]

        route_code: str = row[1]
        route_name: str = row[2]
        route_type: int = row[3]
        route_color: str = row[4]

        route = Route(
            id=route_id,
            code=route_code,
            name=route_name,
            transport_type=TransportType(route_type),
            color=Color(route_color),
        )

        result = {
            "id": route.id,
            "code": route.code,
            "name": route.name,
            "transport_type": route.transport_type.value,
            "color": str(route.color.original()),
        }

        return result
