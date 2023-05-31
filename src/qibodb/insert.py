"""Insert new document."""
import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pymongo import MongoClient

from qibodb.dbs.models import read_model

from .dbs import Database, Collection


def insert(
    paths: list[Path], db: Database, coll: Optional[Collection], client: MongoClient
):
    if coll is None:
        return insert_db(paths, db, client)

    return insert_coll(paths, db, coll, client)


def documents(objs: tuple[BaseModel]) -> list[dict]:
    """Create insertable documents from models."""
    return [json.loads(obj.json()) for obj in objs]


def insert_db(paths: list[Path], db: Database, client: MongoClient):
    pass


def insert_coll(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    # Validate the documents
    objs = tuple(coll.value.parse_file(doc) for doc in paths)
    docs = documents(objs)

    # actually insert
    results = client[db.name][coll.name].insert_many(docs)

    readcls = read_model(coll.value)
    print(results.inserted_ids)
    print(docs)
    return [readcls(id=id_, **doc) for id_, doc in zip(results.inserted_ids, docs)]
