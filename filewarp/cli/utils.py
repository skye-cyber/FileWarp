import time
import sys
import click
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

from rich import box
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    # BarColumn,
    # TaskProgressColumn,
)
from ._entry_ import console
from .banners import display_banner


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


def show_quick_commands():
    """Show quick command reference"""
    table = Table(title="Quick Commands", box=box.ROUNDED, border_style="blue")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Example", style="yellow")

    commands = [
        ("convert-doc", "Convert documents", "filewarp convert-doc file.docx --to pdf"),
        (
            "convert-audio",
            "Convert audio files",
            "filewarp convert-audio song.mp3 --to wav",
        ),
        (
            "convert-video",
            "Convert videos",
            "filewarp convert-video video.mp4 --to mkv",
        ),
        (
            "convert-image",
            "Convert images",
            "filewarp convert-image photo.jpg --to png",
        ),
        ("ocr", "Extract text from images", "filewarp ocr image.png"),
        ("pdf-join", "Join PDF files", "filewarp pdf-join file1.pdf file2.pdf"),
        ("scan", "Scan PDF for text", "filewarp scan document.pdf"),
    ]

    for cmd, desc, example in commands:
        table.add_row(cmd, desc, example)

    console.print(table)


def display_version():
    """Display version with style"""
    import importlib.metadata

    try:
        __version__ = importlib.metadata.version("filewarp")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "unknown"

    version_text = Text()
    version_text.append("Filemac ", style="bold cyan")
    version_text.append(__version__, style="bold green")
    version_text.append(" • Advanced File Management", style="dim")

    panel = Panel(Align.center(version_text), border_style="blue", padding=(1, 2))
    console.print(panel)


# Utility Functions
def show_supported_formats(format_type: str):
    """Show supported formats for a specific conversion type"""
    try:
        if format_type == "document":
            from ..utils.formats import create_doc_formats_table

            # console.print("\n[bold]📄 Document Formats:[/]")
            console.print(create_doc_formats_table())
            console.print("")

        elif format_type == "audio":
            from ..utils.formats import create_audio_formats_table

            # console.print("\n[bold]🎵 Audio Formats:[/]")
            console.print(create_audio_formats_table())
            console.print("")

        elif format_type == "video":
            from ..utils.formats import create_video_formats_table

            # console.print("\n[bold]🎬 Video Formats:[/]")
            # Call the function if it returns a table, otherwise assume it's a table object
            table = create_video_formats_table()
            console.print(table if callable(table) else table)
            console.print("")

        elif format_type == "image":
            from ..utils.formats import create_image_formats_table

            # console.print("\n[bold]🖼️ Image Formats:[/]")
            console.print(create_image_formats_table())
            console.print("")

    except ImportError as e:
        console.print(f"[yellow]Format tables not available: {e}[/]")


class FileWarpGroup(click.Group):
    """Custom Click Group that displays banner with help"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store console instance
        self.console = console

    def get_command(self, ctx, cmd_name):
        """Get command and store its metadata"""
        cmd = super().get_command(ctx, cmd_name)
        if cmd:
            # Store the command's format table type in context for later use
            if hasattr(cmd.callback, "_format_table_type"):
                ctx.obj = ctx.obj or {}
                ctx.obj["format_table_type"] = cmd.callback._format_table_type
        return cmd

    def get_help(self, ctx):
        """Override get_help to include banner"""
        return super().get_help(ctx)

    def format_help(self, ctx, formatter):
        """Override format_help to include banner and quick commands"""

        # Check if we have a format table type stored in context
        if ctx.obj and ctx.obj.get("format_table_type"):
            format_type = ctx.obj["format_table_type"]
            show_supported_formats(format_type)

        # Show quick commands for main help (no subcommand)
        else:
            display_banner()
            self.show_quick_commands()

        # Show main help
        super().format_help(ctx, formatter)

    def format_commands(self, ctx, formatter):
        """Override to add quick commands for main help"""
        # Call parent first
        super().format_commands(ctx, formatter)

        # Show quick commands for main help (no specific command)
        if not ctx.obj or not ctx.obj.get("format_table_type"):
            self.show_quick_commands()

    def main(self, *args, **kwargs):
        """Override main to handle help display"""
        try:
            # Check if this is a help invocation before processing
            if any(arg in sys.argv for arg in ["--help", "-h"]):
                # Show banner immediately for help commands
                # display_banner()

                # Check if it's a subcommand help
                if len(sys.argv) > 1 and sys.argv[1] not in ["--help", "-h"]:
                    from click import Context

                    cmd_name = sys.argv[1]
                    cmd = self.get_command(Context(self), cmd_name)

                    # Show format table if command has metadata
                    if cmd and hasattr(cmd.callback, "_format_table_type"):
                        format_type = cmd.callback._format_table_type
                        show_supported_formats(format_type)

            return super().main(*args, **kwargs)
        except SystemExit as e:
            if e.code == 0:  # Help exit
                sys.exit(0)
            raise

    def main_old(self, *args, **kwargs):
        """Override main to handle help display"""
        try:
            return super().main(*args, **kwargs)
        except SystemExit as e:
            # If it's a help exit (code 0), we've already shown banner and tables
            if e.code == 0:
                sys.exit(0)
            raise

    def show_quick_commands(self):
        """Show quick command reference"""
        table = Table(title="Quick Commands", box=box.ROUNDED, border_style="blue")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Example", style="yellow")

        commands = [
            (
                "convert-doc",
                "Convert documents",
                "filewrap convert-doc file.docx --to pdf",
            ),
            (
                "convert-audio",
                "Convert audio files",
                "filewrap convert-audio song.mp3 --to wav",
            ),
            (
                "convert-video",
                "Convert videos",
                "filewrap convert-video video.mp4 --to mkv",
            ),
            (
                "convert-image",
                "Convert images",
                "filewrap convert-image photo.jpg --to png",
            ),
            ("ocr", "Extract text from images", "filewrap ocr image.png"),
            ("pdf-join", "Join PDF files", "filewrap pdf-join file1.pdf file2.pdf"),
            ("--help", "Show help for any command", "filewrap convert-doc --help"),
        ]

        for cmd, desc, example in commands:
            table.add_row(cmd, desc, example)

        self.console.print(table)
        self.console.print(
            "\n[dim]Use 'filewrap COMMAND --help' for specific command options[/]\n"
        )


def with_format_table(format_type):
    """Decorator to show format table for specific commands (lets default help run)"""

    def decorator(f):
        # We don't override the command's behavior
        # Just attach metadata for the group to use
        f._format_table_type = format_type
        return f

    return decorator
