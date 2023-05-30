from enum import Enum
from itertools import chain
from typing import Union

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


def identifier(db: Database, coll: Collection) -> str:
    return f"{db.name}.{coll.name}"


def collection(identifier: str):
    """Infer collection from name.

    For example::

        >>> collection("platform_qpu")
        (Database.platform, platform.Collection.qpu)

    """
    dbname, collection = identifier.split(".")
    db = Database[dbname]

    return (db, db.value[collection])
