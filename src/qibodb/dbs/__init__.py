from enum import Enum
from itertools import chain
from typing import Optional, Union

from . import platform, calibration


class Database(Enum):
    platform = platform.Collection
    procedure = calibration.Collection

    @classmethod
    def collections(cls):
        return list(chain(*([(db, coll) for coll in db.value] for db in cls)))

    @classmethod
    def identifiers(cls):
        return [identifier(db, coll) for db, coll in cls.collections()]


Collection = Union[platform.Collection, calibration.Collection]


def identifier(db: Database, coll: Optional[Collection] = None) -> str:
    if coll is None:
        return db.name
    return f"{db.name}.{coll.name}"


def collection(identifier: str) -> tuple[Database, Optional[Collection]]:
    """Infer collection from name.

    For example::

        >>> collection("platform.qpu")
        (Database.platform, platform.Collection.qpu)

    """
    elems = identifier.split(".")
    try:
        dbname, collection = elems
    except ValueError:
        if len(elems) > 1:
            raise ValueError
        dbname = elems[0]
        collection = None

    db = Database[dbname]
    coll = db.value[collection] if collection else None

    return (db, coll)
