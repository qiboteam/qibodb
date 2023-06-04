"""Platform supporting hardware execution."""
from ..models import InsertModel
from ..schema import Schema
from .package import Qibolab
from .qpu import QPU


class Platform(InsertModel):
    """A lab platform, spanning QPU and instruments involved."""

    qpu: QPU
    package: Qibolab


class Collection(Schema):
    """Store data for lab."""

    # pylint: disable=invalid-enum-extension
    # https://github.com/pylint-dev/pylint/issues/6887
    QPU = QPU
    PACKAGE = Qibolab
    PLATFORM = Platform

    __bundles__ = ["PLATFORM"]
    __default__ = "PLATFORM"
