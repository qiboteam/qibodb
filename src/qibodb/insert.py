"""Insert new document."""
from pymongo import MongoClient

from .dbs import Database, Collection


def insert(documents: list[dict], db: Database, coll: Collection, client: MongoClient):
    # Validate the documents
    objs = [coll.value(**doc) for doc in documents]

    print(documents)
    print(objs)
    return
    inserted = client[db.name][coll.name].insert_many(documents)

    # TODO: return a *read* object
    return objs, inserted.inserted_ids
