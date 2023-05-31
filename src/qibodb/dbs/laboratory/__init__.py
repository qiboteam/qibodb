"""Platform supporting hardware execution."""
from enum import Enum

from .instrument import Instrument, InstrumentCalibration
from .package import Qibolab
from .qpu import QPU, QPUCalibration


class Collection(Enum):
    qpu = QPU
    qpuconfig = QPUCalibration
    instrument = Instrument
    instrconfig = InstrumentCalibration
    package = Qibolab
