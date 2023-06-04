"""Retrieve document."""

import click
from rich import print_json

from ..conversion import documents, notnull
from ..dbs import IDENTIFIER_DESCR, collection
from ..get import get
from .base import command
from .settings import client


@command.command("show")
@click.argument("ids", nargs=-1)
@click.option("--in", "in_", required=True, help=IDENTIFIER_DESCR)
def show(ids: list[str], in_: str):
    """Show document in database collection."""
    db, coll = collection(in_)

    print_json(data=documents(notnull(get(ids, db, coll, client()))))
