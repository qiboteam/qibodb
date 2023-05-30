"""Track Qibocal versions."""
from pydantic import BaseModel


class Qibocal(BaseModel):
    version: str
