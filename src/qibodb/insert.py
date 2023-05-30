"""Insert new document."""
from pymongo import MongoClient

from .dbs import Database, Collection

def collection(name: str) -> tuple[Database, Collection]:
    """Infer collection from name.

    For example::

        >>> collection("platform_qpu")
        (Database.platform, platform.Collection.qpu)

    """
    dbname, collection = name.split("_")
    db = Database[dbname]

    return (db, db.value[collection])

def insert(document: dict, db: Database, collection: Collection, client: MongoClient):
    obj = collection.value(document)

    client[db.name][collection.name].insert_one(document)

    return obj
