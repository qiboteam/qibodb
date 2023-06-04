"""Convert among formats."""
import json
from typing import Optional, TypeVar

from pydantic import BaseModel

from .dbs.bundle import bundle_model
from .dbs.models import InsertModel, ReadModel, read_model


def documents(objs: tuple[BaseModel, ...]) -> tuple[dict, ...]:
    """Create insertable documents from models."""
    return tuple(json.loads(obj.json()) for obj in objs)


Elem = TypeVar("Elem")


def notnull(elems: tuple[Optional[Elem], ...]) -> tuple[Elem, ...]:
    """Filter out null elements."""
    return tuple(el for el in elems if el is not None)


def read_models(
    docs: tuple[Optional[dict], ...], model: type[InsertModel], bundle: bool = False
) -> tuple[Optional[ReadModel], ...]:
    """Convert database documents to read models."""
    if bundle:
        model = bundle_model(model)
    readcls = read_model(model)
    objs: list[Optional[ReadModel]] = []

    for doc in docs:
        if doc is None:
            objs.append(None)
            continue
        doc["id"] = doc["_id"]
        del doc["_id"]
        objs.append(readcls(**doc))

    return tuple(objs)
