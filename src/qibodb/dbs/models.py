"""Base models and dynamic tools."""
import inspect
from datetime import datetime
from typing import Any, NewType, Optional

from bson.objectid import ObjectId
from pydantic import BaseConfig, BaseModel, Field, create_model


class InsertModel(BaseModel):
    ctime: datetime = Field(default_factory=datetime.utcnow)

    class Config(BaseConfig):
        frozen = True


UpdateModel = NewType("UpdateModel", BaseModel)
ReadModel = NewType("ReadModel", BaseModel)


def ssignature(type_: type) -> dict[str, Any]:
    """Simplified signature."""
    signature = inspect.signature(type_)
    return {attr: par.annotation for attr, par in signature.parameters.items()}


def dynamic_model(name: str, config: type[BaseConfig], **fields: Any):
    return create_model(
        name,
        **fields,
        __config__=config,
        __base__=None,
        __module__=__name__,
        __validators__={},
        __cls_kwargs__={},
    )


def update_model(insert_model: type[InsertModel]) -> type[UpdateModel]:
    fields = {attr: (Optional[ann], None) for attr, ann in ssignature(insert_model).items()}
    del fields["ctime"]
    config = insert_model.Config

    model = dynamic_model(insert_model.__name__, config, **fields)
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


def read_model(insert_model: type[InsertModel]) -> type[ReadModel]:
    fields = {
        "id": (PyObjectId, ...),
        **{attr: (ann, ...) for attr, ann in ssignature(insert_model).items()},
    }
    config = insert_model.Config
    config.json_encoders = {ObjectId: str}

    model = dynamic_model(insert_model.__name__, config, **fields)
    return model
