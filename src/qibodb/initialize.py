from pathlib import Path
import logging
import shutil
import subprocess

_logger = logging.getLogger(__name__)

MONGOPORT = 27017
QIBOPORT = 9160

CONTAINER = "qibodb"
IMAGE = "docker.io/library/mongo:latest"


def podman_exe():
    path = shutil.which("podman")
    if path is None:
        raise FileNotFoundError()

    return path


def podman(command: str):
    args = [podman_exe()] + command.split(" ")
    _logger.warn(" ".join(args))
    subprocess.run(args)


def initdb(data: Path):
    """Run container with a DB instance.

    `data` is supposed to be an absolute path. If it does not exist, it is
    created, otherwise the content is erased.

    """
    try:
        shutil.rmtree(data, ignore_errors=True)
    except PermissionError:
        podman(f"unshare rm -rf {data}")
    data.mkdir()

    podman(f"unshare chown 1000:1000 {data}")
    name = f"--name {CONTAINER}"
    port = f"-p {QIBOPORT}:{MONGOPORT}"
    volume = f"-v {data}:/data/db:Z,U"
    podman(f"run -dt {name} {port} {volume} {IMAGE}")


def startdb():
    podman(f"start {CONTAINER}")


def stopdb():
    podman(f"stop {CONTAINER}")
