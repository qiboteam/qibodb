"""Track Qibolab versions."""
from ..models import InsertModel


class Qibolab(InsertModel):
    """Package reference.

    It could be both a released version number or a branch in the Git repo.

    """

    version: str
