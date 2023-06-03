"""Track Qibolab versions."""
from datetime import datetime
from typing import NewType

from pydantic import Field

from ..models import InsertModel

Version = NewType("Version", str)


class Qibolab(InsertModel):
    """Package reference.

    It could be both a released version number or a branch in the Git repo.

    """

    version: Version
    supersedes: list[tuple[Version, datetime]] = Field(default=[])
