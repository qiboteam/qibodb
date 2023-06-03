"""Common patterns in database management."""
from enum import Enum
from typing import TypeVar

# TODO: not required any longer in py3.11
# https://docs.python.org/3/library/typing.html#typing.Self
_SubSchema = TypeVar("_SubSchema", bound="Schema")


class Schema(Enum):
    """Database interface."""

    __default__: str = ""
    __bundles__: list[str] = []

    # TODO: not required any longer in py3.11
    # https://docs.python.org/3/howto/enum.html#private-names
    # pylint: disable=invalid-name
    _ignore_ = ["__default__", "__bundles__"]

    @classmethod
    def default(cls: type[_SubSchema]) -> _SubSchema:
        """Define the default collection for the database."""
        return cls[cls.__default__]

    @classmethod
    def is_bundle(cls, collection) -> bool:
        """Determine if the given collection is a bundle.

        A *bundle* is just an internal name for a document only consisting of
        references to documents in other collections.

        It is the only allowed mechanism to introduce relations among
        documents.

        """
        return collection.name in cls.__bundles__
