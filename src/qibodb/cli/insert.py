"""Insert document."""
from pathlib import Path

import click
from rich import print_json

from ..conversion import documents, notnull
from ..dbs import IDENTIFIER_DESCR, collection
from ..insert import insert
from .base import command, load, path
from .settings import client


@command.command("insert")
@click.argument("docs", nargs=-1, type=path(exists=True, dir_okay=False))
@click.option("--in", "in_", required=True, help=IDENTIFIER_DESCR)
def insert_(docs: list[Path], in_: str):
    """Insert document in database collection."""
    db, coll = collection(in_)

    loaded = load(docs)
    print_json(data=documents(notnull(insert(loaded, db, coll, client()))))
