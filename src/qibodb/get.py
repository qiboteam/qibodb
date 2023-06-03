"""Get existing document."""
from typing import Optional

from bson.objectid import ObjectId
from pymongo import MongoClient

from .conversion import read_models
from .dbs import Collection, Database


def get(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from collection."""
    _get = get_bundle if db.value.is_bundle(coll) else get_coll

    return _get(ids, db, coll, client)


def get_coll(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from simple collection."""
    results: list[Optional[dict]] = [
        client[db.name.lower()][coll.name.lower()].find_one({"_id": ObjectId(id)})
        for id in ids
    ]
    return read_models(tuple(results), coll.value)


def get_bundle(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from bundle collection."""
    return get_coll(ids, db, coll, client)
