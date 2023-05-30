"""QPU specs and calibration."""
from enum import Enum
from typing import Union

QubitId = Union[int, str]
Topology = list[tuple[QubitId, QubitId]]


class ResonatorType(Enum):
    dim2 = "2D"
    dim3 = "3D"


class QPU:
    description: str
    qubits: list[QubitId]
    topology: Topology

    resonator_type: ResonatorType


class QPUCalibration:
    sampling_rate: int
    repetition_duration: int
