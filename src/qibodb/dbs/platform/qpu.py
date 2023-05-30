"""QPU specs and calibration."""
from enum import Enum
from typing import Union

from sqlalchemy.orm import Mapped

from .base import Base

QubitId = Union[int, str]
Topology = list[tuple[QubitId, QubitId]]


class ResonatorType(Enum):
    dim2 = "2D"
    dim3 = "3D"


class QPU(Base):
    __tablename__ = "qpu"

    description: Mapped[str]
    qubits: Mapped[list[QubitId]]
    topology: Mapped[Topology]

    resonator_type: Mapped[ResonatorType]


class QPUCalibration(Base):
    __tablename__ = "qpu_calibration"

    sampling_rate: Mapped[int]
    repetition_duration: Mapped[int]
