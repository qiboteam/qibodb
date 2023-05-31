from enum import Enum
from itertools import chain
from typing import Optional, Union

from . import calibration, laboratory


class Database(Enum):
    """Available databases."""

    platform = laboratory.Collection
    procedure = calibration.Collection

    @classmethod
    def collections(cls):
        """All available collections."""
        return list(chain(*([(db, coll) for coll in db.value] for db in cls)))

    @classmethod
    def identifiers(cls):
        """All available collections identifiers."""
        return [identifier(db, coll) for db, coll in cls.collections()]


Collection = Union[laboratory.Collection, calibration.Collection]
"""A collection from one of the available databases."""


def identifier(db: Database, coll: Optional[Collection] = None) -> str:
    """Create database/collection identifier.

    For collections the identifier consists of a string
    ``"database.collection"``, while for databases correspons just to their
    name.

    """
    if coll is None:
        return db.name
    return f"{db.name}.{coll.name}"


def _parse_id(identifier: str) -> tuple[str, Optional[str]]:
    """Parse string identifier in its components."""
    elems = identifier.split(".")
    db = elems[0]
    if len(elems) == 2:
        return (db, elems[1])
    if len(elems) == 1:
        return (db, None)
    raise ValueError


def collection(identifier: str) -> tuple[Database, Optional[Collection]]:
    """Infer collection from name.

    For example::

        >>> collection("platform.qpu")
        (Database.platform, platform.Collection.qpu)

        >>> collection("platform")
        (Database.platform, None)

    """
    dbname, collection = _parse_id(identifier)

    db = Database[dbname]
    coll = db.value[collection] if collection else None

    return (db, coll)
