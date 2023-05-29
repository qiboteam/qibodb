from pathlib import Path

import click

from ..initialize import initdb, startdb, stopdb


@click.group("qibodb")
def command():
    pass


def path(**kwargs):
    return click.Path(path_type=Path, resolve_path=True, **kwargs)


@command.command("init")
@click.argument("data", type=path(file_okay=False))
def init(data: Path):
    initdb(data)


@command.command("start")
def start(data: Path):
    startdb()


@command.command("stop")
def stop(data: Path):
    stopdb()
