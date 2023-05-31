"""Insert document."""
from pathlib import Path

import click
from rich.pretty import pprint

from ..conversion import documents
from ..dbs import collection
from ..insert import insert
from .base import command, path
from .settings import client


@command.command("insert")
@click.argument("docs", nargs=-1, type=path(exists=True, dir_okay=False))
@click.option("--in", "in_", required=True)
def insert_(docs: list[Path], in_: str):
    db, coll = collection(in_)

    pprint(documents(insert(docs, db, coll, client())), indent_guides=False)
