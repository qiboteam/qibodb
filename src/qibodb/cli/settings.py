"""Establish QiboDB settings."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Set defaults, resolve the environment."""

    mongo_port = 27017
    qibo_port = 9160

    container_name = "qibodb"
    container_image = "docker.io/library/mongo:latest"

    class Config:
        env_prefix = "qibodb_"


settings = Settings()
"""Global settings instance (CLI runs are one-shot)."""


def vars(settings: Settings):
    return {
        f"{settings.Config.env_prefix}{k}".upper(): v
        for k, v in settings.dict().items()
    }
