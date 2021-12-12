"""Module to store the main service functions."""

from typing import Any, Dict, List, Union

from now8_api.domain import Route, TransportType
from now8_api.service.service import Service, exclude
from pydantic.color import Color
from pypika import Query, Table


class RouteService(Service):

    routes_cache: Dict[str, Dict[str, Any]] = None

    async def initialize_routes_cache(self) -> None:
        """Initialize `routes_cache` if undefined."""
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

        self.routes_cache = result

    async def all_routes(
        self, keys_to_exclude: List[str] = None
    ) -> Dict[str, Dict[str, Union[str, float, dict]]]:
        """Return all the routes of the city.

        Returns:
            List of dictionaries with the route ID, transport type, way,
            name, coordinates and zone of each route.
        """
        if self.routes_cache is None:
            await self.initialize_routes_cache()

        return exclude(
            dict_of_dicts=self.routes_cache, keys_to_exclude=keys_to_exclude
        )

    async def route_info(self, route_id: str) -> Dict[str, Union[str, float]]:
        """Return the route information.

        Arguments:
            route_id: Route identifier.

        Returns:
            Dictionary with the route ID, transport type, way, name,
                coordinates and zone.

        Raises:
            ValueError: If the `route_id` does not match any route.
        """
        if self.routes_cache is None:
            await self.initialize_routes_cache()

        return self.routes_cache[route_id]
