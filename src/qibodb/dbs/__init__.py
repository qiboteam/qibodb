from enum import Enum
from itertools import chain
from typing import Optional, Union

from . import calibration, laboratory


class Database(Enum):
    """Available databases."""

    PLATFORM = laboratory.Collection
    PROCEDURE = calibration.Collection

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


def _parse_id(identifier_: str) -> tuple[str, Optional[str]]:
    """Parse string identifier in its components."""
    elems = identifier_.split(".")
    db = elems[0]
    if len(elems) == 2:
        return (db, elems[1])
    if len(elems) == 1:
        return (db, None)
    raise ValueError


def collection(identifier_: str) -> tuple[Database, Collection]:
    """Infer collection from name.

    For example::

        >>> collection("platform.qpu")
        (Database.platform, platform.Collection.qpu)

        >>> collection("platform")
        (Database.platform, None)

    """
    dbname, collname = _parse_id(identifier_)

    db = Database[dbname.upper()]
    coll = db.value[collname.upper()] if collname is not None else db.value.default()

    return (db, coll)
