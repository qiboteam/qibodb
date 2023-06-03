"""Insert new document."""
from pathlib import Path

from pymongo import MongoClient

from .conversion import documents, read_models
from .dbs import Collection, Database


def insert(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    """Insert document in collection."""
    _insert = insert_bundle if db.value.is_bundle(coll) else insert_coll

    return _insert(paths, db, coll, client)


def insert_coll(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    """Insert document in simple collection."""
    # Validate the documents
    objs = tuple(coll.value.parse_file(doc) for doc in paths)
    docs = documents(objs)

    # actually insert
    _ = client[db.name.lower()][coll.name.lower()].insert_many(docs)

    return read_models(docs, coll.value)


def insert_bundle(
    paths: list[Path], db: Database, coll: Collection, client: MongoClient
):
    """Insert document in bundle collection."""
    return insert_coll(paths, db, coll, client)
