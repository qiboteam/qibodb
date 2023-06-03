"""Platform supporting hardware execution."""
from ..models import InsertModel
from ..schema import Schema
from .package import Qibolab
from .qpu import QPU


class Platform(InsertModel):
    qpu: QPU
    package: Qibolab


class Collection(Schema):
    qpu = QPU
    package = Qibolab
    platform = Platform

    __bundles__ = ["platform"]
    __default__ = "platform"
