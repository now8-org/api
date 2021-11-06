"""Module to store the PostgreSQL engine."""

from typing import List

import asyncpg
from now8_api.data.database import SqlEngine


class PostgresqlSqlEngine(SqlEngine):
    """PostgreSQL engine class."""

    async def execute_query(self, query: str, *args) -> List:
        """Return the result of executing the passed query.

        Arguments:
            query: Query to perform.

        Returns:
            The result of executing the passed query.
        """
        db_conf = self.get_db_conf()
        db_conf["database"] = db_conf.pop("dbname")
        conn = await asyncpg.connect(**db_conf, timeout=3)

        query_result = await conn.fetch(query, *args)

        await conn.close()

        return query_result
