"""Track Qibolab versions."""
from ..models import InsertModel


class Qibolab(InsertModel):
    version: str
