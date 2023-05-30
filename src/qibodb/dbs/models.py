"""Base models and dynamic tools."""
import inspect
from datetime import datetime
from typing import NewType, Optional, Type

from pydantic import BaseModel, Field, create_model


class InsertModel(BaseModel):
    ctime: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True


UpdateModel = NewType("UpdateModel", BaseModel)
ReadModel = NewType("ReadModel", BaseModel)


def ssignature(type: Type):
    """Simplified signature."""
    signature = inspect.signature(type)
    return {attr: par.annotation for attr, par in signature.parameters.items()}


def update_model(insert_model: Type[InsertModel]) -> Type[UpdateModel]:
    fields = {
        attr: (Optional[ann], None) for attr, ann in ssignature(insert_model).items()
    }
    del fields["ctime"]
    config = insert_model.Config

    model = create_model(insert_model.__name__, **fields, __config__=config)
    return model


def read_model(insert_model: Type[InsertModel]) -> Type[ReadModel]:
    fields = {
        "id": (int, ...),
        **{attr: (ann, ...) for attr, ann in ssignature(insert_model).items()},
    }
    config = insert_model.Config

    model = create_model(insert_model.__name__, **fields, __config__=config)
    return model
