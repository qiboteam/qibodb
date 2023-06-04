"""Establish QiboDB settings."""
from pydantic import BaseSettings
from pymongo import MongoClient


class Settings(BaseSettings):
    """Set defaults, resolve the environment."""

    host = "localhost"
    qibo_port = 9160
    mongo_port = 27017

    container_name = "qibodb"
    container_image = "docker.io/library/mongo:latest"

    class Config:
        """Pydantic settings configurations."""

        env_prefix = "qibodb_"


settings = Settings()
"""Global settings instance (CLI runs are one-shot)."""


def variables(settings_: Settings):
    """Report available variables from given settings."""
    return {
        f"{settings_.Config.env_prefix}{k}".upper(): v
        for k, v in settings_.dict().items()
    }


def client():
    """Return a new MongoDB client instance.

    The instance is configured with globally available settings.

    See also
    --------
    :data:`settings`

    """
    return MongoClient(settings.host, settings.qibo_port)
