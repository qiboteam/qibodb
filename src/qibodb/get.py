"""Get existing document."""
from typing import Any, Optional

import pymongo.database
from bson.objectid import ObjectId
from pymongo import MongoClient

from .conversion import read_models
from .dbs import Collection, Database
from .dbs.bundle import ElementCategory


def get(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from collection."""
    _get = bundle if db.value.is_bundle(coll) else collection

    return _get(ids, db, coll, client)


def collection(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from simple collection."""
    results: list[Optional[dict]] = [
        client[db.name.lower()][coll.name.lower()].find_one({"_id": ObjectId(id)})
        for id in ids
    ]
    return read_models(tuple(results), coll.value)


def _dropid(doc: Optional[dict]):
    if doc is None:
        return None
    del doc["_id"]
    return doc


def element(value: Any, db: pymongo.database.Database):
    """Retrieve referenced element from its collection."""
    cat = ElementCategory.from_hint(type(value))

    if cat is ElementCategory.SCALAR:
        return _dropid(db.dereference(value))
    if cat is ElementCategory.LIST:
        return [_dropid(db.dereference(ref)) for ref in value]
    if cat is ElementCategory.DICT:
        return {name: _dropid(db.dereference(ref)) for name, ref in value.items()}

    raise ValueError


def bundle(ids: list[str], db: Database, coll: Collection, client: MongoClient):
    """Retrieve document from bundle collection."""
    results: list[Optional[dict]] = [
        client[db.name.lower()][coll.name.lower()].find_one({"_id": ObjectId(id)})
        for id in ids
    ]

    docs = []
    for res in results:
        if res is None:
            docs.append(None)
            continue
        doc = {}
        for name, value in res.items():
            if name in {"_id", "ctime"}:
                doc[name] = value
            else:
                doc[name] = element(value, client[db.name.lower()])
        docs.append(doc)

    return read_models(tuple(docs), coll.value)
