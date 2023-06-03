"""QPU specs and calibration."""
from enum import Enum
from typing import Union

from ..models import InsertModel

QubitId = Union[int, str]
Topology = list[tuple[QubitId, QubitId]]


class ResonatorType(Enum):
    """Type of resonator cavity."""

    DIM2 = "2D"
    DIM3 = "3D"


class Settings(InsertModel):
    """QPU settings."""

    sampling_rate: int
    repetition_duration: int


class QPU(InsertModel):
    """Quantum Processing Unit representation.

    This contains both defining parameters and those that can be calibrated.

    """

    description: str
    qubits: list[QubitId]
    topology: Topology

    resonator_type: ResonatorType

    settings: Settings
