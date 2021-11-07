"""Module to store the PostgreSQL engine."""

import socket
from typing import List

import asyncpg
from now8_api.data.database import SqlEngine
from tenacity import retry, stop_after_attempt


class PostgresqlSqlEngine(SqlEngine):
    """PostgreSQL engine class."""

    @retry(stop=stop_after_attempt(3))
    async def execute_query(self, query: str, *args) -> List:
        """Return the result of executing the passed query.

        Arguments:
            query: Query to perform.

        Returns:
            The result of executing the passed query.
        """
        db_conf = self.get_db_conf()
        db_conf["database"] = db_conf.pop("dbname")

        try:
            conn = await asyncpg.connect(**db_conf, timeout=3)
        except socket.gaierror as error:
            raise ConnectionError(
                f"Can't connect to database: {db_conf}."
            ) from error

        query_result = await conn.fetch(query, *args)

        await conn.close()

        return query_result
