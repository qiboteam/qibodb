"""QPU specs and calibration."""
from enum import Enum
from typing import Union

from pydantic import Field

from ..models import InsertModel

QubitId = Union[int, str]
"""Qubit identifier type."""
Topology = list[tuple[QubitId, QubitId]]
"""Connections among qubits."""


class ResonatorType(str, Enum):
    """Type of resonator cavity."""

    DIM2 = "2D"
    DIM3 = "3D"


class Settings(InsertModel):
    """QPU settings."""

    nshots: int
    sampling_rate: int
    relaxation_time: int


class NativeGateType(str, Enum):
    """Available types of native gates."""

    RX = "RX"
    MZ = "MZ"


class GateChannel(str, Enum):
    """Channels on which the gate is implemented."""

    READOUT = "ro"
    DRIVE = "qd"


class NativeGate(InsertModel):
    """Native gate pulse parameters."""

    duration: int
    amplitude: float
    frequency: int
    shape: str
    type: GateChannel
    start: int
    phase: int


class Mixer(InsertModel):
    """Mixer parameters."""

    drive_g: float
    drive_phi: float
    readout_g: float
    readout_phi: float


class QubitCharacterization(InsertModel):
    """'Qubit properties.'"""

    readout_frequency: int
    drive_frequency: float
    t1: float = Field(alias="T1")
    t2: float = Field(alias="T2")
    sweetspot: float
    filter: dict
    threshold: float
    iq_angle: float
    mixer: Mixer


class Qubit(InsertModel):
    """Qubit information."""

    native_gates: dict[NativeGateType, NativeGate]
    characterization: QubitCharacterization


class QPU(InsertModel):
    """Quantum Processing Unit representation.

    This contains both defining parameters and those that can be calibrated.

    """

    description: str
    topology: Topology

    resonator_type: ResonatorType

    settings: Settings

    qubits: dict[QubitId, Qubit]
