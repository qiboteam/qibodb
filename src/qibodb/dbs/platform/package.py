"""Track Qibolab versions."""
from pydantic import BaseModel


class Qibolab(BaseModel):
    version: str
