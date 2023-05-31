"""Base models and dynamic tools."""
import inspect
from datetime import datetime
from typing import NewType, Optional, Type

from pydantic import BaseModel, Field, create_model
from bson import ObjectId


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


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def read_model(insert_model: Type[InsertModel]) -> Type[ReadModel]:
    fields = {
        "_id": (PyObjectId, ...),
        **{attr: (ann, ...) for attr, ann in ssignature(insert_model).items()},
    }
    config = insert_model.Config

    model = create_model(insert_model.__name__, **fields, __config__=config)
    return model
