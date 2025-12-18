#!/usr/bin/env python3
"""
FileMAC Enhanced CLI Application

This module provides an enhanced CLI interface using Rich and pyperclip
for better user experience while maintaining compatibility with the
original CLI.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
# Import existing FileMAC components
from filemac.cli.cli import OperationMapper, argsdev as original_argsdev
from filemac.utils.colors import fg, bg, rs
from filemac.core.exceptions import FileSystemError, FilemacError

# Rich imports for enhanced UI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.box import ROUNDED
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt, Confirm

# Clipboard integration
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Initialize Rich console with custom theme
RESET = rs

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "debug": "magenta",
    "prompt": "bold blue",
    "header": "bold white on blue",
    "footer": "white on grey15"
})

console = Console(theme=custom_theme)


class RichConsoleUtils:
    """Utility class for Rich console operations"""

    @staticmethod
    def print_info(message: str):
        """Print informational message"""
        console.print(f"[info]ℹ {message}[/info]")

    @staticmethod
    def print_success(message: str):
        """Print success message"""
        console.print(f"[success]✓ {message}[/success]")

    @staticmethod
    def print_error(message: str):
        """Print error message"""
        console.print(f"[error]❌ {message}[/error]")

    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        console.print(f"[warning]⚠ {message}[/warning]")

    @staticmethod
    def print_debug(message: str):
        """Print debug message"""
        console.print(f"[debug]🐞 {message}[/debug]")

    @staticmethod
    def print_header(title: str, subtitle: str = ""):
        """Print formatted header"""
        panel = Panel.fit(
            f"[bold]{title}[/bold]\n[dim]{subtitle}[/dim]" if subtitle else f"[bold]{title}[/bold]",
            border_style="blue",
            title="[header]FileMAC[/header]",
            subtitle="[footer]Advanced File Processing[/footer]"
        )
        console.print(panel)


class ClipboardManager:
    """Clipboard operations manager"""

    @staticmethod
    def is_available() -> bool:
        """Check if clipboard is available"""
        return CLIPBOARD_AVAILABLE

    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """Copy text to system clipboard"""
        if not CLIPBOARD_AVAILABLE:
            RichConsoleUtils.print_warning("Clipboard not available on this system")
            return False

        try:
            pyperclip.copy(text)
            RichConsoleUtils.print_success("Copied to clipboard!")
            return True
        except Exception as e:
            RichConsoleUtils.print_error(f"Failed to copy to clipboard: {str(e)}")
            return False

    @staticmethod
    def paste_from_clipboard() -> Optional[str]:
        """Get text from system clipboard"""
        if not CLIPBOARD_AVAILABLE:
            RichConsoleUtils.print_warning("Clipboard not available on this system")
            return None

        try:
            content = pyperclip.paste()
            return content if content and content.strip() else None
        except Exception as e:
            RichConsoleUtils.print_error(f"Failed to access clipboard: {str(e)}")
            return None


class EnhancedHelpSystem:
    """Enhanced help system with Rich formatting"""

    COMMAND_CATEGORIES = {
        "Document Conversion": [
            ("--convert_doc", "Convert documents between formats", "filemac --convert_doc file.docx -to pdf"),
            ("--doc2image", "Convert documents to images", "filemac --doc2image file.pdf -to png"),
            ("--html2word", "Convert HTML to Word", "filemac --html2word index.html"),
            ("--markdown2docx", "Convert Markdown to DOCX", "filemac --markdown2docx file.md"),
        ],
        "Image Processing": [
            ("--convert_image", "Convert image formats", "filemac --convert_image file.jpg -to png"),
            ("--resize_image", "Resize images", "filemac --resize_image file.png -to_size 2mb"),
            ("--image2pdf", "Convert images to PDF", "filemac --image2pdf image1.jpg image2.jpg"),
            ("--image2word", "Convert images to Word", "filemac --image2word image1.jpg"),
            ("--image2gray", "Convert to grayscale", "filemac --image2gray image.jpg"),
        ],
        "Audio Processing": [
            ("--convert_audio", "Convert audio formats", "filemac --convert_audio file.mp3 -to wav"),
            ("--extract_audio", "Extract audio from video", "filemac -xA video.mp4"),
            ("--AudioJoin", "Join audio files", "filemac --AudioJoin file1.mp3 file2.mp3"),
        ],
        "Video Processing": [
            ("--convert_video", "Convert video formats", "filemac --convert_video file.mp4 -to mkv"),
            ("--Analyze_video", "Analyze video", "filemac --Analyze_video video.mp4"),
        ],
        "PDF Operations": [
            ("--pdfjoin", "Join PDF files", "filemac --pdfjoin file1.pdf file2.pdf"),
            ("--extract_pages", "Extract PDF pages", "filemac --extract_pages file.pdf 1 3 5"),
            ("--scan", "Scan PDF text", "filemac --scan file.pdf"),
        ],
        "OCR & Text": [
            ("--ocr", "Extract text from images", "filemac --ocr image.png"),
            ("--scanAsImg", "Scan PDF as images", "filemac --scanAsImg file.pdf"),
            ("--Richtext2word", "Advanced text to Word", "filemac --Richtext2word file.txt"),
        ],
        "Miscellaneous": [
            ("--voicetype", "Voice typing", "filemac --voicetype"),
            ("--record", "Record audio", "filemac --record"),
            ("--version", "Show version", "filemac --version"),
        ]
    }

    @classmethod
    def show_help(cls):
        """Display enhanced help with categorized commands"""
        RichConsoleUtils.print_header("FileMAC Help System", "Advanced file conversion toolkit")

        for category, commands in cls.COMMAND_CATEGORIES.items():
            table = Table(
                title=f"📁 {category}",
                show_header=True,
                header_style="bold magenta",
                box=ROUNDED,
                border_style="blue"
            )

            table.add_column("Command", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")
            table.add_column("Example", style="green")

            for cmd, desc, example in commands:
                table.add_row(cmd, desc, example)

            console.print(table)
            console.print()  # Add spacing between categories

        # Additional information
        info_panel = Panel.fit(
            "[bold yellow]Tip:[/bold yellow] Use [cyan]--help[/cyan] with any command for detailed usage.\n\n"
            "[bold yellow]Clipboard:[/bold yellow] Use [cyan]--clipboard[/cyan] flag to enable clipboard integration.\n\n"
            "[bold yellow]Examples:[/bold yellow]\n"
            "  filemac --convert_doc document.docx -to pdf\n"
            "  filemac --image2pdf *.jpg --clipboard\n"
            "  filemac --ocr image.png --copy-results",
            title="[bold]Additional Information[/bold]",
            border_style="yellow",
            subtitle="Usage Tips and Examples"
        )
        console.print(info_panel)

    @classmethod
    def show_quick_start(cls):
        """Show quick start guide"""
        RichConsoleUtils.print_header("Quick Start Guide", "Get started with FileMAC")

        quick_start_content = """
[bold]1. Basic Conversion:[/bold]
  filemac --convert_doc document.docx -to pdf
  filemac --convert_image photo.jpg -to png

[bold]2. Batch Processing:[/bold]
  filemac --convert_audio *.mp3 -to wav
  filemac --image2pdf /path/to/images/

[bold]3. Advanced Features:[/bold]
  filemac --resize_image large.jpg -to_size 1mb
  filemac --pdfjoin file1.pdf file2.pdf -order AAB

[bold]4. Clipboard Integration:[/bold]
  filemac --convert_doc file.docx --clipboard
  filemac --ocr image.png --copy-results

[bold]5. Help and Information:[/bold]
  filemac --help
  filemac --version
"""

        panel = Panel.fit(
            quick_start_content,
            title="[bold]Quick Start[/bold]",
            border_style="green",
            subtitle="Common FileMAC Commands"
        )
        console.print(panel)


class ProgressManager:
    """Progress bar management for operations"""

    @staticmethod
    def create_progress_bar(description: str = "Processing..."):
        """Create a standardized progress bar"""
        return Progress(
            SpinnerColumn("dots", style="cyan"),
            TextColumn("[progress.description]{task.description}", style="white"),
            BarColumn(complete_style="green", finished_style="blue", pulse_style="magenta"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style="yellow"),
            TextColumn("[blue]{task.completed}[/blue]/[green]{task.total}[/green]", justify="right"),
            TextColumn("•", style="dim"),
            TextColumn("[progress.elapsed]{task.elapsed:>.1f}s", style="white"),
            TextColumn("•", style="dim"),
            TextColumn("[progress.remaining]{task.remaining:>.1f}s remaining", style="white"),
            transient=True
        )

    @staticmethod
    def show_progress(operation_name: str, items: List[Any], callback: callable):
        """Show progress bar for an operation"""
        with ProgressManager.create_progress_bar(description=operation_name) as progress:
            task = progress.add_task(operation_name, total=len(items))

            for item in items:
                callback(item)
                progress.update(task, advance=1)


class OperationSummary:
    """Operation summary and reporting"""

    @staticmethod
    def show_summary(operation_name: str, results: List[Dict[str, Any]]):
        """Display operation summary"""
        success_count = sum(1 for r in results if r.get('success', False))
        error_count = len(results) - success_count
        total_files = len(results)

        # Create summary table
        summary_table = Table(show_header=True, box=ROUNDED)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="white")

        summary_table.add_row("Operation", operation_name)
        summary_table.add_row("Files Processed", str(total_files))
        summary_table.add_row("Success", f"[green]{success_count}[/green]")
        summary_table.add_row("Errors", f"[red]{error_count}[/red]")
        summary_table.add_row("Success Rate",
                              f"[green]{success_count / total_files * 100:.1f}%[/green]" if total_files > 0 else "N/A")

        # Create error details if any
        error_details = ""
        if error_count > 0:
            error_details = "\n[bold red]Error Details:[/bold red]\n"
            for i, result in enumerate(results, 1):
                if not result.get('success', True):
                    error_details += f"{i}. [red]{result.get('file', 'Unknown')}[/red]: {result.get('error', 'Unknown error')}\n"

        # Create summary panel
        panel = Panel.fit(
            summary_table,
            title=f"[bold]Operation Summary: {operation_name}[/bold]",
            border_style="green" if error_count == 0 else "yellow",
            subtitle=f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        console.print(panel)

        if error_details:
            console.print(error_details)

        # Offer to copy summary to clipboard
        summary_text = f"FileMAC Operation Summary - {operation_name}\n"
        summary_text += f"Processed: {total_files} files\n"
        summary_text += f"Success: {success_count}\n"
        summary_text += f"Errors: {error_count}\n"
        summary_text += f"Success Rate: {success_count / total_files * 100:.1f}%\n"

        if error_count > 0:
            summary_text += "\nErrors:\n"
            for result in results:
                if not result.get('success', True):
                    summary_text += f"- {result.get('file', 'Unknown')}: {result.get('error', 'Unknown error')}\n"

        if ClipboardManager.is_available() and Confirm.ask("Copy summary to clipboard?"):
            ClipboardManager.copy_to_clipboard(summary_text)


class EnhancedOperationMapper(OperationMapper):
    """Enhanced operation mapper with Rich features"""

    def __init__(self, parser, args, remaining_args):
        super().__init__(parser, args, remaining_args)
        self.clipboard_enabled = getattr(args, 'clipboard', False)
        self.show_progress_bars = True

    def handle_help(self):
        """Enhanced help handling"""
        if not self.args and not self.remaining_args:
            EnhancedHelpSystem.show_help()
            return True
        return False

    def handle_quick_start(self):
        """Handle quick start guide"""
        if hasattr(self.args, 'quick_start') and self.args.quick_start:
            EnhancedHelpSystem.show_quick_start()
            return True
        return False

    def get_file_input(self, prompt: str) -> Union[str, List[str]]:
        """Get file input with optional clipboard support"""
        if self.clipboard_enabled and ClipboardManager.is_available():
            RichConsoleUtils.print_info("Clipboard mode enabled - checking for file paths...")

            clipboard_content = ClipboardManager.paste_from_clipboard()
            if clipboard_content:
                files = [f.strip() for f in clipboard_content.split('\n') if f.strip()]
                if files:
                    RichConsoleUtils.print_success(f"Found {len(files)} file paths from clipboard")

                    # Show preview
                    if Confirm.ask("Show clipboard content preview?", default=True):
                        preview_table = Table(title="Clipboard Content Preview", box=ROUNDED)
                        preview_table.add_column("Index", style="cyan")
                        preview_table.add_column("File Path", style="white")

                        for i, file in enumerate(files, 1):
                            preview_table.add_row(str(i), file)

                        console.print(preview_table)

                    return files

        # Fallback to original behavior
        return super().get_file_input(prompt)

    def show_operation_start(self, operation_name: str):
        """Show operation start message"""
        RichConsoleUtils.print_info(f"Starting {operation_name}...")

    def show_operation_complete(self, operation_name: str, results: List[Dict[str, Any]]):
        """Show operation completion message"""
        OperationSummary.show_summary(operation_name, results)

    def show_progress(self, operation_name: str, items: List[Any], callback: callable):
        """Show progress for operation"""
        if self.show_progress_bars:
            ProgressManager.show_progress(operation_name, items, callback)
        else:
            # Fallback to original behavior
            for item in items:
                callback(item)


def enhanced_argsdev():
    """
    Enhanced CLI entry point with Rich interface

    This function provides the main entry point for the enhanced FileMAC CLI
    with Rich formatting and additional features while maintaining
    compatibility with the original CLI.
    """
    try:
        # Initialize Rich console and display welcome message
        RichConsoleUtils.print_header(
            "🚀 FileMAC Enhanced CLI",
            "Advanced File Processing with Rich Interface"
        )

        # Create parser with enhanced help
        parser = argparse.ArgumentParser(
            description="Filemac: Advanced file management tool with Rich interface",
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="Use --help for detailed command information or --quick-start for examples"
        )

        # Add enhanced flags
        parser.add_argument(
            "--clipboard",
            action="store_true",
            help="Enable clipboard integration for input/output operations"
        )

        parser.add_argument(
            "--quick-start",
            action="store_true",
            help="Show quick start guide with common examples"
        )

        parser.add_argument(
            "--no-progress",
            action="store_true",
            help="Disable progress bars for cleaner output"
        )

        parser.add_argument(
            "--copy-results",
            action="store_true",
            help="Copy operation results to clipboard automatically"
        )

        # Add original arguments (this would be imported or duplicated from original)
        # For now, we'll handle the original arguments through the existing system

        # Parse known arguments first
        args, remaining_args = parser.parse_known_args()

        # Handle quick start
        if args.quick_start:
            EnhancedHelpSystem.show_quick_start()
            sys.exit(0)

        # Handle help
        if '--help' in remaining_args or '-h' in remaining_args:
            EnhancedHelpSystem.show_help()
            sys.exit(0)

        # Check if user wants original CLI
        if '--original' in remaining_args:
            RichConsoleUtils.print_info("Switching to original CLI interface...")
            original_argsdev()
            return

        # Initialize enhanced operation mapper
        # Note: In a real implementation, we would need to properly integrate
        # with the existing argument parsing system

        RichConsoleUtils.print_info("Enhanced CLI mode activated")
        RichConsoleUtils.print_info("Note: Some features are still under development")

        # For now, fall back to original CLI but with enhanced features
        # This is a temporary measure until full integration is complete

        # Create a basic enhanced experience
        if args.clipboard:
            RichConsoleUtils.print_success("Clipboard integration enabled")

        if args.no_progress:
            RichConsoleUtils.print_info("Progress bars disabled")

        # Show enhanced help if no arguments provided
        if not any(vars(args).values()) and not remaining_args:
            EnhancedHelpSystem.show_help()
            sys.exit(0)

        # Fall back to original CLI for actual operations
        # This maintains compatibility while we develop the enhanced version
        RichConsoleUtils.print_info("Processing with enhanced interface...")
        original_argsdev()

    except KeyboardInterrupt:
        RichConsoleUtils.print_warning("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        RichConsoleUtils.print_error(f"Unexpected error: {str(e)}")
        if Confirm.ask("Show detailed error information?", default=False):
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    enhanced_argsdev()
