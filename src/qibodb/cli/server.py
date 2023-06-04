"""Manage a database server instance in a container.

Requires ``podman`` to be installed.

"""
import logging
import shutil
import subprocess
from pathlib import Path

import click

from .base import command, path
from .settings import settings

_logger = logging.getLogger(__name__)


def podman_exe():
    """Locate podman executable."""
    path_ = shutil.which("podman")
    if path_ is None:
        raise FileNotFoundError()

    return path_


def podman(subcommand: str):
    """Run podman command."""
    args = [podman_exe()] + subcommand.split(" ")
    _logger.info(" ".join(args))
    subprocess.run(args, check=True)


def initdb(data: Path):
    """Run container with a DB instance.

    `data` is supposed to be an absolute path. If it does not exist, it is
    created, otherwise the content is erased.

    """
    try:
        shutil.rmtree(data)
    except OSError as err:
        if not isinstance(err, PermissionError):
            raise err
        podman(f"unshare rm -rf {data}")
    data.mkdir()

    container = settings.container_name
    image = settings.container_image
    qibo_port = settings.qibo_port
    mongo_port = settings.mongo_port

    podman(f"unshare chown 1000:1000 {data}")
    name = f"--name {container}"
    port = f"-p {qibo_port}:{mongo_port}"
    volume = f"-v {data}:/data/db:Z,U"
    podman(f"run -dt {name} {port} {volume} {image}")


def startdb():
    """Restart the container."""
    container = settings.container_name
    podman(f"start {container}")


def stopdb():
    """Stop the container."""
    container = settings.container_name
    podman(f"stop {container}")


@command.group("server")
def server():
    """Server management utilities."""


@server.command("init")
@click.argument("data", type=path(file_okay=False))
def init(data: Path):
    """Initialize new container with a MongoDB server."""
    initdb(data)


@server.command("start")
def start():
    """Start the server."""
    startdb()


@server.command("stop")
def stop():
    """Stop the server."""
    stopdb()
