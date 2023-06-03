from enum import Enum


class Schema(Enum):
    __default__: str = ""
    __bundles__: list[str] = []

    # TODO: not required any longer in py3.11
    # https://docs.python.org/3/howto/enum.html#private-names
    _ignore_ = ["__default__", "__bundles__"]

    @classmethod
    def default(cls):
        return cls[cls.__default__]

    @classmethod
    def is_bundle(cls, collection):
        return collection.name in cls.__bundles__
