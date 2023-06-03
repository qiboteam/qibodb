"""Calibration procedure."""
from ..schema import Schema
from .package import Qibocal


class Collection(Schema):
    package = Qibocal
