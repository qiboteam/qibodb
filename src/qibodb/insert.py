"""Insert new document."""
from pathlib import Path
from typing import Optional

from pymongo import MongoClient

from .conversion import documents, read_models
from .dbs import Collection, Database


def insert(paths: list[Path], db: Database, coll: Optional[Collection], client: MongoClient):
    if coll is None:
        return insert_db(paths, db, client)

    return insert_coll(paths, db, coll, client)


def insert_db(paths: list[Path], db: Database, client: MongoClient):
    return read_models((), None)


def insert_coll(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    # Validate the documents
    objs = tuple(coll.value.parse_file(doc) for doc in paths)
    docs = documents(objs)

    # actually insert
    _ = client[db.name][coll.name].insert_many(docs)

    return read_models(docs, coll.value)
