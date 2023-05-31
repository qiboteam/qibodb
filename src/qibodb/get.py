"""Get existing document."""
from typing import Optional

from pymongo import MongoClient

from .dbs import Database, Collection


def get(
    paths: list[str], db: Database, coll: Optional[Collection], client: MongoClient
):
    if coll is None:
        return get_db(paths, db, client)

    return get_coll(paths, db, coll, client)


def get_db(paths: list[str], db: Database, client: MongoClient):
    pass


def get_coll(paths: list[str], db: Database, coll: Collection, client: MongoClient):
    pass
