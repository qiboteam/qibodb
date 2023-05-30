from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


def utc():
    return datetime.now(timezone.utc)


UID = Annotated[int, mapped_column(primary_key=True, unique=True)]
Timestamp = Annotated[datetime, mapped_column(default=utc)]


class Base(DeclarativeBase, MappedAsDataclass):
    uid: Mapped[UID]
    ctime: Mapped[Timestamp]
    mtime: Mapped[Timestamp] = mapped_column(onupdate=utc)
