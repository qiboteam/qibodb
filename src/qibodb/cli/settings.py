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
        env_prefix = "qibodb_"


settings = Settings()
"""Global settings instance (CLI runs are one-shot)."""


def vars(settings: Settings):
    return {
        f"{settings.Config.env_prefix}{k}".upper(): v
        for k, v in settings.dict().items()
    }


def client():
    return MongoClient(settings.host, settings.qibo_port)
