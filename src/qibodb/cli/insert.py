"""Insert document."""
from pathlib import Path

import click
from rich.pretty import pprint

from .base import command, path
from .settings import client
from ..dbs import collection
from ..insert import insert


@command.command("insert")
@click.argument("docs", nargs=-1, type=path(exists=True, dir_okay=False))
@click.option("--in", "in_", required=True)
def insert_(docs: list[Path], in_: str):
    db, coll = collection(in_)

    pprint(insert(docs, db, coll, client()))
