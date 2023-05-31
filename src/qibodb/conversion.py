"""Convert among formats."""
import json
from typing import Optional

from pydantic import BaseModel

from .dbs.models import InsertModel, ReadModel, read_model


def documents(objs: tuple[BaseModel, ...]) -> tuple[dict, ...]:
    """Create insertable documents from models."""
    return tuple(json.loads(obj.json()) for obj in objs)


def read_models(docs: tuple[Optional[dict], ...], model: type[InsertModel]) -> tuple[Optional[ReadModel], ...]:
    """Convert database documents to read models."""
    readcls = read_model(model)
    objs: list[Optional[ReadModel]] = []

    for doc in docs:
        if doc is None:
            objs.append(doc)
            continue
        doc["id"] = doc["_id"]
        del doc["_id"]
        objs.append(readcls(**doc))

    return tuple(objs)
