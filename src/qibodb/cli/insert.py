"""Insert document."""
from pathlib import Path

import click
from rich import print_json

from ..conversion import documents
from ..dbs import IDENTIFIER_DESCR, collection
from ..insert import insert
from .base import command, path
from .settings import client


@command.command("insert")
@click.argument("docs", nargs=-1, type=path(exists=True, dir_okay=False))
@click.option("--in", "in_", required=True, help=IDENTIFIER_DESCR)
def insert_(docs: list[Path], in_: str):
    """Insert document in database collection."""
    db, coll = collection(in_)

    print_json(data=documents(insert(docs, db, coll, client())))
