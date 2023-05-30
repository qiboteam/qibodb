from enum import Enum

from . import platform, calibration

class Database(Enum):
    platform = platform.Collection
    procedure = calibration.Collection
