from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_port = 27017
    qibo_port = 9160

    container_name = "qibodb"
    container_image = "docker.io/library/mongo:latest"

    class Config:
        env_prefix = "qibodb_"


settings = Settings()
