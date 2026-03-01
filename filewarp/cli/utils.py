import time
import click
from rich.text import Text
from rich.table import Table
from rich import box
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    # BarColumn,
    # TaskProgressColumn,
)
from ._entry_ import console


def create_progress_spinner(message: str):
    """Create a progress spinner"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    )


def animate_processing(message: str):
    """Decorator to animate processing"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with console.status(f"[bold cyan]{message}", spinner="dots"):
                time.sleep(0.5)  # Small delay for effect
                result = func(*args, **kwargs)
            console.print(f"[bold green]✓[/] {message} completed!")
            return result

        return wrapper

    return decorator


class RichHelpFormatter(click.HelpFormatter):
    """Custom help formatter with rich formatting"""

    def write_usage(self, prog, args="", prefix="Usage: "):
        usage = Text()
        usage.append(prefix, style="bold green")
        usage.append(prog, style="bold cyan")
        if args:
            usage.append(f" {args}", style="yellow")
        console.print(usage)

    def write_dl(self, rows, col_max=30, col_spacing=2):
        table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        table.add_column("Command", style="bold cyan", no_wrap=True)
        table.add_column("Description", style="white")

        for row in rows:
            table.add_row(row[0], row[1])

        console.print(table)
