"""Base command definition."""
import json
from pathlib import Path
from typing import Iterable

import click
import yaml

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def path(**kwargs):
    """Add common parameters to :class:`click.Path`."""
    return click.Path(path_type=Path, resolve_path=True, **kwargs)


def load(paths: Iterable[Path]) -> list[dict]:
    loaded = []
    for path in paths:
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            doc = json.loads(content)
        elif path.suffix in {".yml", ".yaml"}:
            doc = yaml.safe_load(content)
        else:
            raise ValueError

        loaded.append(doc)
    return loaded


@click.group(context_settings=CONTEXT_SETTINGS)
def command():
    """Base command for the whole CLI."""
