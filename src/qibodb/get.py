"""Get existing document."""
from typing import Optional

from bson import ObjectId
from pymongo import MongoClient

from .dbs import Database, Collection
from .dbs.models import ReadModel, read_model


def get(ids: list[str], db: Database, coll: Optional[Collection], client: MongoClient):
    if coll is None:
        return get_db(ids, db, client)

    return get_coll(ids, db, coll, client)


def get_db(ids: list[str], db: Database, client: MongoClient) -> tuple[ReadModel]:
    pass


def get_coll(
    ids: list[str], db: Database, coll: Collection, client: MongoClient
) -> tuple[ReadModel]:
    results = [client[db.name][coll.name].find_one({"_id": ObjectId(id)}) for id in ids]
    readcls = read_model(coll.value)
    return tuple(readcls(**res) for res in results)
