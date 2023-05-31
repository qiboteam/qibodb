"""Retrieve document."""

import click
from rich import print_json

from ..conversion import documents
from ..dbs import collection
from ..get import get
from .base import command
from .settings import client


@command.command("show")
@click.argument("ids", nargs=-1)
@click.option("--in", "in_", required=True)
def show(ids: list[str], in_: str):
    db, coll = collection(in_)

    print_json(data=documents(get(ids, db, coll, client())))
