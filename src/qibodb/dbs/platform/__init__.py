"""Platform supporting hardware execution."""
from enum import Enum

from .qpu import QPU, QPUCalibration
from .instrument import Instrument, InstrumentCalibration
from .package import Qibolab


class Collection(Enum):
    qpu = QPU
    qpuconfig = QPUCalibration
    instrument = Instrument
    instrconfig = InstrumentCalibration
    package = Qibolab
