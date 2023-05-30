from enum import Enum
from typing import Union

from . import platform, calibration


class Database(Enum):
    platform = platform.Collection
    procedure = calibration.Collection


Collection = Union[platform.Collection, calibration.Collection]
