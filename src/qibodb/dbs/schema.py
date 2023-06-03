"""Common patterns in database management."""
from enum import Enum
from typing import TypeVar

SubSchema = TypeVar("SubSchema", bound="Schema")


class Schema(Enum):
    """Database interface."""

    __default__: str = ""
    __bundles__: list[str] = []

    # TODO: not required any longer in py3.11
    # https://docs.python.org/3/howto/enum.html#private-names
    # pylint: disable=invalid-name
    _ignore_ = ["__default__", "__bundles__"]

    @classmethod
    def default(cls: type[SubSchema]) -> SubSchema:
        return cls[cls.__default__]

    @classmethod
    def is_bundle(cls, collection) -> bool:
        return collection.name in cls.__bundles__
