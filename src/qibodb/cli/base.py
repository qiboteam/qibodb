"""Base command definition."""
from pathlib import Path

import click

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def path(**kwargs):
    """Add common parameters to :class:`click.Path`."""
    return click.Path(path_type=Path, resolve_path=True, **kwargs)


@click.group(context_settings=CONTEXT_SETTINGS)
def command():
    """Base command for the whole CLI."""
