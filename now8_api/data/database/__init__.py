"""Module to store the common objects for the database."""

from abc import ABC, abstractmethod
from os import environ
from typing import Dict, List, Optional

from pydantic import validator
from pydantic.dataclasses import dataclass


@dataclass
class SqlEngine(ABC):
    """SQL engine class.

    Attributes:
        env_prefix: Prefix of the environment variables with the database
            connection parameters.
        name: Name of the database.
        user: User name of the database.
        password: Password of the database.
        host: Host of the database.
        port: Port of the database.
    """

    env_prefix: str = "DB_"
    name: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None

    @validator("name", always=True)
    @classmethod
    def validate_name(cls, value, values):
        """Get name from environment variable if undefined."""
        return (
            environ.get(values["env_prefix"] + "NAME", "postgres")
            if value is None
            else value
        )

    @validator("user", always=True)
    @classmethod
    def validate_user(cls, value, values):
        """Get user from environment variable if undefined."""
        return (
            environ.get(values["env_prefix"] + "USER", "postgres")
            if value is None
            else value
        )

    @validator("password", always=True)
    @classmethod
    def validate_password(cls, value, values):
        """Get password from environment variable if undefined."""
        return (
            environ.get(values["env_prefix"] + "PASS", "postgres")
            if value is None
            else value
        )

    @validator("host", always=True)
    @classmethod
    def validate_host(cls, value, values):
        """Get host from environment variable if undefined."""
        return (
            environ.get(values["env_prefix"] + "HOST", "postgres")
            if value is None
            else value
        )

    @validator("port", always=True)
    @classmethod
    def validate_port(cls, value, values):
        """Get port from environment variable if undefined."""
        return (
            environ.get(values["env_prefix"] + "PORT", "5432")
            if value is None
            else value
        )

    def get_db_conf(self) -> Dict[str, str]:
        """Return the database connection parameters.

        Returns:
            Dictionary with the available database connection parameters.
        """
        return {
            "dbname": str(self.name),
            "user": str(self.user),
            "password": str(self.password),
            "host": str(self.host),
            "port": str(self.port),
        }

    @abstractmethod
    async def execute_query(self, query: str, *args) -> List[tuple]:
        """Return the result of executing the passed query.

        Arguments:
            query: Query to perform.
            args: Query arguments.

        Returns:
            The result of executing the passed query.
        """
