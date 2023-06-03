"""Calibration procedure."""
from ..schema import Schema
from .package import Qibocal


class Collection(Schema):
    """Store data for the calibration process."""

    # pylint: disable=invalid-enum-extension
    # https://github.com/pylint-dev/pylint/issues/6887
    PACKAGE = Qibocal
