"""Insert document"""
import json
from pathlib import Path

import click

from .base import command, path
from .settings import client, vars
from ..dbs import collection
from ..insert import insert


@command.command("insert")
@click.argument("docs", nargs=-1, type=path(exists=True, dir_okay=False))
@click.option("--in", "in_")
def insert_(docs: list[Path], in_: str):
    db, coll = collection(in_)

    contents = [json.loads(p.read_text()) for p in docs]
    insert(contents, db, coll, client())
