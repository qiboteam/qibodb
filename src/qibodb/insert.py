"""Insert new document."""
from datetime import datetime
from pathlib import Path
from typing import Any

import pymongo.collection
from bson.dbref import DBRef
from pymongo import MongoClient

from .conversion import documents, read_models
from .dbs import Collection, Database
from .dbs.bundle import ElementCategory, collections, extract


def insert(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    """Insert document in collection."""
    _insert = bundle if db.value.is_bundle(coll) else collection

    return _insert(paths, db, coll, client)


def collection(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    """Insert document in simple collection."""
    # Validate the documents
    objs = tuple(coll.value.parse_file(doc) for doc in paths)
    docs = documents(objs)

    # actually insert
    _ = client[db.name.lower()][coll.name.lower()].insert_many(docs)

    return read_models(docs, coll.value)


def element(
    name: str,
    value: Any,
    cat: ElementCategory,
    template: dict,
    coll: pymongo.collection.Collection,
):
    """Insert a referenced element in its collection.

    The template is modified in place, setting the object ID of the inserted
    document.

    """
    doc = documents((value,))[0]
    result = coll.insert_one(doc)

    dbref = DBRef(coll.name, result.inserted_id)

    # if it's a scalar, just assign the result
    if cat is ElementCategory.SCALAR:
        template[name] = dbref
    # in case of a list, append it
    elif cat is ElementCategory.LIST:
        template[name].append(dbref)
    # for dicts, set it on the first non-empty field
    elif cat is ElementCategory.DICT:
        for key, val in template[name].items():
            if val is None:
                template[name][key] = dbref
                break


def bundle(paths: list[Path], db: Database, coll: Collection, client: MongoClient):
    """Insert document in bundle collection."""
    objs = tuple(coll.value.parse_file(doc) for doc in paths)

    # insert elements, and collect references
    docs = []
    for obj in objs:
        ref, template = extract(obj)
        for value, type_, name, cat in ref:
            elcoll = collections(db.value)[type_]
            element(name, value, cat, template, client[db.name.lower()][elcoll.lower()])
        template["ctime"] = datetime.utcnow()
        docs.append(template)

    # insert the actual bundle
    docs_ = tuple(docs)
    client[db.name.lower()][coll.name.lower()].insert_many(docs_)

    return read_models(docs_, coll.value, bundle=True)
