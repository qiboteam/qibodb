"""Get existing document."""
from typing import Optional

from bson.objectid import ObjectId
from pymongo import MongoClient

from .conversion import read_models
from .dbs import Collection, Database


def get(ids: list[str], db: Database, coll: Optional[Collection], client: MongoClient):
    if coll is None:
        return get_db(ids, db, client)

    return get_coll(ids, db, coll, client)


def get_db(ids: list[str], db: Database, client: MongoClient):
    return read_models((), None)


def get_coll(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    results: list[Optional[dict]] = [client[db.name][coll.name].find_one({"_id": ObjectId(id)}) for id in ids]
    return read_models(tuple(results), coll.value)
