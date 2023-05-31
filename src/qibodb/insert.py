"""Insert new document."""
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pymongo import MongoClient

from .dbs import Database, Collection


def insert(
    docs: list[Path], db: Database, coll: Optional[Collection], client: MongoClient
):
    if coll is None:
        return insert_db(docs, db, client)

    return insert_coll(docs, db, coll, client)


def documents(objs: tuple[BaseModel]) -> Iterator[dict]:
    """Create insertable documents from models."""
    return (json.loads(obj.json()) for obj in objs)


def insert_db(docs: list[Path], db: Database, client: MongoClient):
    pass


def insert_coll(docs: list[Path], db: Database, coll: Collection, client: MongoClient):
    # Validate the documents
    objs = tuple(coll.value.parse_file(doc) for doc in docs)

    # actually insert
    inserted = client[db.name][coll.name].insert_many(documents(objs))

    # TODO: return a *read* object
    return objs, inserted.inserted_ids
