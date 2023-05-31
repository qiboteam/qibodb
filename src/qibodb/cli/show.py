"""Retrieve document."""

import click
from rich.pretty import pprint

from .base import command
from .settings import client
from ..dbs import collection
from ..get import get


@command.command("show")
@click.argument("ids", nargs=-1)
@click.option("--in", "in_", required=True)
def show(ids: list[str], in_: str):
    db, coll = collection(in_)

    pprint(get(ids, db, coll, client()))
