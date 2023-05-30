"""Track Qibocal versions."""
from ..models import InsertModel


class Qibocal(InsertModel):
    version: str
