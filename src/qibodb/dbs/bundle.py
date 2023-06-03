"""Manage bundle collections.

A *bundle* is just an internal name for a document only consisting of
references to documents in other collections.

It is the only allowed mechanism to introduce relations among
documents.

"""
import inspect
from enum import Enum, auto
from functools import cache
from typing import Any, NewType, get_args, get_origin

from bson.dbref import DBRef
from bson.objectid import ObjectId

from .models import InsertModel, dynamic_model, ssignature


@cache
def collections(db: type[Enum]):
    return {var.value: var.name for var in db}


class ElementCategory(Enum):
    """A bundle element.

    It represents the kind of reference: single document or a collection.

    """

    SCALAR = auto()
    LIST = auto()
    DICT = auto()

    @classmethod
    def from_hint(cls, annotation: Any):
        """Infer the element kind from type hint."""
        if not inspect.isclass(annotation):
            annotation = get_origin(annotation)

        if issubclass(annotation, dict):
            return cls.DICT
        if issubclass(annotation, list):
            return cls.LIST
        return cls.SCALAR


def extract(bundle: InsertModel):
    """Extract elements from a bundle document."""
    template: dict[str, Any] = {}
    referenced: list[tuple[Any, type, str, ElementCategory]] = []
    for name, field in bundle.__fields__.items():
        if name == "ctime":
            continue
        cat = ElementCategory.from_hint(field.annotation)
        value = getattr(bundle, name)
        if cat is ElementCategory.SCALAR:
            template[name] = None
            referenced.append((value, type(value), name, cat))
        elif cat is ElementCategory.LIST:
            template[name] = []
            type_ = get_args(field.annotation)[0]
            referenced.extend([(value, type_, name, cat)])
        elif cat is ElementCategory.DICT:
            template[name] = {}
            type_ = get_args(field.annotation)[1]
            referenced.extend([(value, type_, name, cat)])

    return (referenced, template)


BundleModel = NewType("ReadModel", InsertModel)


class PyDBRef(DBRef):
    """A validated MongoDB database reference."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Validate DBRef with ``bson``."""
        if isinstance(value, DBRef):
            return value

        if not ObjectId.is_valid(value[1]):
            raise ValueError("Invalid objectid")
        return DBRef(value[0], value[1])

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="array", prefixItems=[{"type": "string"}] * 2)


def bundle_model(insert_model: type[InsertModel]) -> type[BundleModel]:
    fields = {}
    for attr, ann in ssignature(insert_model).items():
        if attr == "ctime":
            continue

        cat = ElementCategory.from_hint(ann)
        if cat is ElementCategory.SCALAR:
            fields[attr] = (PyDBRef, ...)
        elif cat is ElementCategory.LIST:
            fields[attr] = (list[PyDBRef], ...)
        elif cat is ElementCategory.DICT:
            keytype = get_args(ann)[0]
            fields[attr] = (dict[keytype, PyDBRef], ...)
        else:
            raise ValueError

    config = insert_model.Config
    config.json_encoders = {DBRef: lambda ref: [ref.collection, ref.id]}

    model = dynamic_model(insert_model.__name__, config, **fields)
    return model
