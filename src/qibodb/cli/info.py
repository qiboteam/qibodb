"""Info."""
import rich
import rich.box
import rich.padding
from rich.table import Table

from .base import command
from .settings import settings, vars


@command.group("info")
def info():
    """Retrieve database meta-information."""


@info.command("settings")
def settings_():
    table = Table(title="QiboDB settings", box=rich.box.HORIZONTALS)
    table.add_column("Name", style="magenta")
    table.add_column("Resolved value", style="cyan", justify="center")

    for name, value in vars(settings).items():
        table.add_row(name, str(value))

    rich.print(rich.padding.Padding(table, (1, 5)))
