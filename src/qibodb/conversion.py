"""Convert among formats."""
import json

from pydantic import BaseModel

from .dbs import Collection
from .dbs.models import ReadModel, read_model


def documents(objs: tuple[BaseModel]) -> tuple[dict]:
    """Create insertable documents from models."""
    return tuple(json.loads(obj.json()) for obj in objs)


def read_models(docs: tuple[dict], coll: Collection) -> tuple[ReadModel]:
    """Convert database documents to read models."""
    readcls = read_model(coll.value)
    return tuple(readcls(**doc) for doc in docs)
