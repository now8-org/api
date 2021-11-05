import pytest
from now8_api.data.database.postgres import PostgresqlSqlEngine


@pytest.mark.slow
class TestPostgres:
    postgresql_sql_engine = PostgresqlSqlEngine(env_prefix="TEST_DB_")

    @pytest.mark.asyncio
    async def test_execute_query(self):
        query = "SELECT $1"
        result = await self.postgresql_sql_engine.execute_query(query, "hello")
        assert isinstance(result, list)
        # there should be one rows
        assert len(result) == 1
        # each row should have 1 column
        assert len(result[0]) == 1
        # the only element should be 1
        assert result[0][0] == "hello"
