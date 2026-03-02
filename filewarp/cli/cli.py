#!/usr/bin/env python3

import os
import sys

# from functools import lru_cache
from pathlib import Path

# from typing import Optional, List, Tuple

# Rich imports for amazing UI
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress,
    # SpinnerColumn,
    # TextColumn,
    # BarColumn,
    # TaskProgressColumn,
)

# from rich.syntax import Syntax
# from rich.tree import Tree
# from rich.layout import Layout
# from rich.live import Live
from rich.text import Text
from rich import box
# from rich.prompt import Prompt, Confirm

# from rich.markdown import Markdown
from rich.align import Align

# from rich.columns import Columns
# from rich.style import Style

# Click for better CLI handling
import click
# from click.decorators import decorator
# from click.core import Context, Option

# Local imports
from ..core.document import DocConverter
from ..core.pdf.core import PageExtractor
from ..core.exceptions import FileSystemError, FilemacError

# from ..utils.colors import fg, bg, rs
from ..utils.simple import logger
from .banners import display_banner
from ._entry_ import console
from .utils import (
    # create_progress_spinner,
    animate_processing,
    # RichHelpFormatter,
)

try:
    from audiobot.cli import cli as audiobot_cli
except ImportError:
    pass


# RESET = rs
_entry_ = PageExtractor._entry_


@click.group(
    invoke_without_command=True,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option("--version", "-V", is_flag=True, help="Show software version and exit.")
@click.option(
    "--no-resume",
    is_flag=True,
    default=False,
    help="Don't resume previous file operation",
)
@click.option(
    "--threads", "-t", type=int, default=3, help="Number of threads for operations"
)
@click.pass_context
def cli(ctx, version, no_resume, threads):
    """Filemac: Advanced File Management & Conversion Tool"""

    if version:
        display_version()
        ctx.exit()

    # Store context values
    ctx.ensure_object(dict)
    ctx.obj["no_resume"] = no_resume
    ctx.obj["threads"] = threads

    if ctx.invoked_subcommand is None:
        display_banner()
        console.print(
            "\n[bold]Welcome to Filemac![/] Use [cyan]filewarp --help[/] for commands.\n"
        )
        show_quick_commands()


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
    version_text = Text()
    version_text.append("Filemac ", style="bold cyan")
    version_text.append("v2.0.1", style="bold green")
    version_text.append(" • Advanced File Management", style="dim")

    panel = Panel(Align.center(version_text), border_style="blue", padding=(1, 2))
    console.print(panel)


# Document Conversion Commands
@cli.command(name="convert-doc")
@click.argument("files", nargs=-1, required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
@click.option("--isolate", "-iso", help="Isolate specific file types")
@click.option(
    "--use-extras", "-X", is_flag=True, help="Use alternative conversion method"
)
@click.pass_context
@animate_processing("Document conversion")
def convert_document(ctx, files, to, isolate, use_extras):
    """Convert documents between formats (PDF, DOCX, etc.)"""

    if files[0] == "help":
        show_supported_formats("document")
        return

    console.print(
        Panel(
            f"[bold]Converting[/] {len(files)} file(s) to [cyan]{to}[/]",
            border_style="green",
        )
    )

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Converting...", total=len(files))

        from .converter import MethodMappingEngine, DirectoryConverter, Batch_Audiofy

        if len(files) == 1 and os.path.isdir(files[0]):
            converter = DirectoryConverter(
                files[0], to, ctx.obj["no_resume"], ctx.obj["threads"], isolate
            )
            converter._unbundle_dir_()
        else:
            for file in files:
                if os.path.isfile(file):
                    ev = MethodMappingEngine(file, to)
                    ev.document_eval()
                progress.update(task, advance=1)


# Audio Commands
@cli.command(name="convert-audio")
@click.argument("file", required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
@animate_processing("Audio conversion")
def convert_audio(file, to):
    """Convert audio files between formats (MP3, WAV, etc.)"""

    if file == "help":
        show_supported_formats("audio")
        return

    from ..core.audio.core import AudioConverter

    with console.status(f"[bold cyan]Converting {file} to {to}..."):
        ev = AudioConverter(file, to)
        ev.pydub_conv()

    console.print(f"[bold green]✓[/] Successfully converted to [cyan]{to}[/]")


@cli.command(name="join-audio")
@click.argument("files", nargs=-1, required=True)
@click.option("--output", "-o", help="Output filename")
@animate_processing("Audio joining")
def join_audio(files, output):
    """Join multiple audio files into one"""

    from ..core.audio.core import AudioJoiner

    console.print(
        Panel(f"[bold]Joining[/] {len(files)} audio files", border_style="blue")
    )

    joiner = AudioJoiner(list(files))
    result = joiner.worker()

    console.print(f"[bold green]✓[/] Joined {len(files)} files successfully")


@cli.command(name="extract-audio")
@click.argument("video_file", required=True)
@animate_processing("Audio extraction")
def extract_audio(video_file):
    """Extract audio from video files"""

    from ..core.audio.core import AudioExtracter

    with console.status("[bold cyan]Extracting audio..."):
        vi = AudioExtracter(video_file)
        vi.moviepyextract()

    console.print("[bold green]✓[/] Audio extracted successfully")


# Video Commands
@cli.command(name="convert-video")
@click.argument("file", required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
@animate_processing("Video conversion")
def convert_video(file, to):
    """Convert video files between formats (MP4, MKV, etc.)"""

    if file == "help":
        show_supported_formats("video")
        return

    from ..core.video.core import VideoConverter

    with console.status(f"[bold cyan]Converting {file} to {to}..."):
        ev = VideoConverter(file, to)
        ev.CONVERT_VIDEO()

    console.print(f"[bold green]✓[/] Successfully converted to [cyan]{to}[/]")


@cli.command(name="analyze-video")
@click.argument("video_file", required=True)
def analyze_video(video_file):
    """Analyze video file properties"""

    from ..miscellaneous.video_analyzer import SimpleAnalyzer

    console.print(Panel(f"[bold]Analyzing[/] {video_file}", border_style="cyan"))

    with console.status("[bold cyan]Processing video..."):
        analyzer = SimpleAnalyzer(video_file)
        analyzer.SimpleAnalyzer()


# Image Commands
@cli.command(name="convert-image")
@click.argument("file", required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
@animate_processing("Image conversion")
def convert_image(file, to):
    """Convert image files between formats (PNG, JPG, etc.)"""

    if file == "help":
        show_supported_formats("image")
        return

    from ..core.image.core import ImageConverter

    with console.status(f"[bold cyan]Converting {file} to {to}..."):
        conv = ImageConverter(file, to)
        conv.convert_image()

    console.print(f"[bold green]✓[/] Successfully converted to [cyan]{to}[/]")


@cli.command(name="resize-image")
@click.argument("image_file", required=True)
@click.option("--size", "-s", required=True, help="Target size (e.g., 2mb, 800x600)")
@click.option("--to", "-tf", help="Target format")
@animate_processing("Image resizing")
def resize_image(image_file, size, to):
    """Resize or compress images"""

    from ..core.image.core import ImageCompressor

    res = ImageCompressor(image_file)
    res.resize_image(size)


@cli.command(name="images-to-pdf")
@click.argument("sources", nargs=-1, required=True)
@click.option("--sort", is_flag=True, help="Sort images")
@click.option("--base", is_flag=True, help="Base name for output")
@click.option("--walk", is_flag=True, help="Process subdirectories")
@click.option("--clean", is_flag=True, help="Clean up after processing")
@animate_processing("Image to PDF conversion")
def images_to_pdf(sources, sort, base, walk, clean):
    """Convert images to PDF"""

    from ..core.image.core import ImagePdfConverter

    sources_list = list(sources)

    if len(sources_list) > 1 or os.path.isfile(os.path.abspath(sources_list[0])):
        converter = ImagePdfConverter(image_list=sources_list)
    else:
        converter = ImagePdfConverter(
            input_dir=sources_list[0], order=sort, base=base, walk=walk, clean=clean
        )

    converter.run()


@cli.command(name="images-to-word")
@click.argument("sources", nargs=-1, required=True)
@animate_processing("Image to Word conversion")
def images_to_word(sources):
    """Convert images to Word document"""

    from ..core.image.core import ImageDocxConverter

    sources_list = list(sources)

    if len(sources_list) > 1:
        converter = ImageDocxConverter(image_list=sources_list)
    else:
        converter = ImageDocxConverter(input_dir=sources_list[0])

    converter.run()


@cli.command(name="grayscale")
@click.argument("sources", nargs=-1, required=True)
@animate_processing("Grayscale conversion")
def convert_grayscale(sources):
    """Convert images to grayscale"""

    from ..core.image.core import GrayscaleConverter

    sources_list = list(sources)
    converter = (
        GrayscaleConverter(sources_list)
        if len(sources_list) > 1
        else GrayscaleConverter(sources_list[0])
    )
    converter.run()


# PDF Commands
@cli.command(name="pdf-join")
@click.argument("pdfs", nargs=-1, required=True)
@click.option("--order", "-o", default="AAB", help="Page order pattern")
@animate_processing("PDF joining")
def pdf_join(pdfs, order):
    """Join multiple PDF files"""

    if pdfs[0].lower() == "help":
        from ..utils.helpmaster import pdf_combine_help

        opts, helper, example = pdf_combine_help()
        console.print(Panel(helper, title="PDF Join Help", border_style="blue"))
        console.print(f"[yellow]Example:[/] {example}")
        return

    from ..core.pdf.core import PDFCombine

    console.print(Panel(f"[bold]Joining[/] {len(pdfs)} PDF files", border_style="blue"))

    init = PDFCombine(list(pdfs), None, None, order)
    init.controller()


@cli.command(name="extract-pages")
@click.argument("pdf_file", required=True)
@click.argument("pages", nargs=-1, type=int, required=True)
@animate_processing("Page extraction")
def extract_pages(pdf_file, pages):
    """Extract specific pages from PDF"""

    console.print(f"[bold]Extracting pages[/] {pages} from [cyan]{pdf_file}[/]")

    args = [pdf_file] + [str(p) for p in pages]
    _entry_(args)


@cli.command(name="extract-images")
@click.argument("pdf_file", required=True)
@click.option("--size", help="Image size (e.g., 256x82)")
@animate_processing("Image extraction")
def extract_images(pdf_file, size):
    """Extract images from PDF"""

    from ..core.image.extractor import process_files

    if size:
        size_tuple = tuple([int(x) for x in size.lower().split("x")])
        process_files([pdf_file], tsize=size_tuple)
    else:
        process_files([pdf_file])


@cli.command(name="scan-pdf")
@click.argument("pdf_file", required=True)
def scan_pdf(pdf_file):
    """Scan PDF and extract text"""

    sc = PageExtractor(pdf_file)
    sc.scanPDF()


@cli.command(name="scan-as-image")
@click.argument("pdf_file", required=True)
def scan_as_image(pdf_file):
    """Scan PDF as images then extract text"""

    sc = PageExtractor(pdf_file)
    sc.scanAsImgs()


@cli.command(name="scan-long")
@click.argument("pdf_file", required=True)
@click.option("--separator", "-sep", default="\n", help="Text separator")
def scan_long(pdf_file, separator):
    """Scan document as long image (effective for complex layouts)"""

    sc = PageExtractor(pdf_file, separator)
    sc.scanAsLongImg()


@cli.command(name="pdf-to-long-image")
@click.argument("pdf_file", required=True)
def pdf_to_long_image(pdf_file):
    """Convert PDF to long image"""

    from ..core.pdf.core import PDF2LongImageConverter

    conv = PDF2LongImageConverter(pdf_file)
    conv.preprocess()


# SVG Commands
@cli.command(name="convert-svg")
@click.argument("svg_file", required=True)
@click.option("--to", "-tf", required=True, help="Target format (png, pdf, svg)")
@animate_processing("SVG conversion")
def convert_svg(svg_file, to):
    """Convert SVG files to other formats"""

    from ..core.svg.core import SVGConverter
    from ..utils.file_utils import generate_filename

    converter = SVGConverter()

    converters = {
        "png": converter.to_png,
        "pdf": converter.to_pdf,
        "svg": converter.to_svg,
    }

    convert_func = converters.get(to)
    if not convert_func:
        console.print(f"[bold red]Error:[/] Invalid target format: {to}")
        console.print("Supported formats: [cyan]png[/], [cyan]pdf[/], [cyan]svg[/]")
        return

    output = generate_filename(ext=to, basedir=Path(svg_file))

    convert_func(input_svg=svg_file, output_path=output.as_posix(), is_string=False)

    console.print(f"[bold green]✓[/] Saved to: [cyan]{output}[/]")


# OCR Commands
@cli.command(name="ocr")
@click.argument("images", nargs=-1, required=True)
@click.option("--separator", "-sep", default="\n", help="Text separator")
@animate_processing("OCR processing")
def perform_ocr(images, separator):
    """Extract text from images using OCR"""

    from ..core.ocr import ExtractText

    console.print(
        Panel(f"[bold]Processing[/] {len(images)} image(s)", border_style="cyan")
    )

    ocr = ExtractText(list(images), separator)
    ocr.run()


# Document to Image
@cli.command(name="doc-to-image")
@click.argument("document", required=True)
@click.option("--to", "-tf", required=True, help="Target image format")
@animate_processing("Document to image conversion")
def doc_to_image(document, to):
    """Convert documents to images"""

    conv = DocConverter(document)
    conv.doc2image(to)


# HTML to Word
@cli.command(name="html-to-word")
@click.argument("html_files", nargs=-1, required=True)
@animate_processing("HTML to Word conversion")
def html_to_word(html_files):
    """Convert HTML files to Word documents"""

    from ..core.html import HTML2Word
    from ..utils.file_utils import generate_filename

    converter = HTML2Word()

    for html_file in html_files:
        output = generate_filename(ext="docx", basedir=Path(html_file))

        with console.status(f"[cyan]Converting {Path(html_file).name}..."):
            converter.convert_file(html_file, output)

        console.print(f"[bold green]✓[/] Converted: [cyan]{output}[/]")


# Markdown to Word
@cli.command(name="markdown-to-word")
@click.argument("markdown_file", required=True)
@animate_processing("Markdown to Word conversion")
def markdown_to_word(markdown_file):
    """Convert Markdown to Word with Mermaid rendering"""

    console.print(f"[bold]Converting[/] [cyan]{markdown_file}[/] to Word")


# Text to Word
@cli.command(name="text-to-word")
@click.argument("text_file", required=True)
@click.option("--font-size", default=12, help="Font size")
@click.option("--font-name", default="Times New Roman", help="Font name")
@animate_processing("Text to Word conversion")
def text_to_word(text_file, font_size, font_name):
    """Convert styled text to Word document"""

    from ..core.text.core import StyledText

    init = StyledText(text_file, None, font_size, font_name)
    init.text_to_word()


# Recording and Voice Commands
@cli.command(name="record")
def record_audio():
    """Record audio from microphone"""

    from ..core.recorder import SoundRecorder

    console.print(Panel("[bold]Audio Recording[/]", border_style="red"))
    console.print("[yellow]Press Ctrl+C to stop recording[/]")

    rec = SoundRecorder()
    rec.run()


@cli.command(name="voice-type")
def voice_type():
    """Use voice to type text"""

    from voice.VoiceType import VoiceTypeEngine

    try:
        console.print(Panel("[bold]Voice Typing Active[/]", border_style="green"))
        console.print("[yellow]Speak clearly... Press Ctrl+C to stop[/]")

        engine = VoiceTypeEngine()
        engine.start()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Voice typing stopped[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


# Utility Functions
def show_supported_formats(format_type: str):
    """Show supported formats for a specific conversion type"""

    if format_type == "document":
        from ..utils.formats import SUPPORTED_DOC_FORMATS

        table = Table(title="Supported Document Formats", box=box.ROUNDED)
        table.add_column("Format", style="cyan")
        for fmt in SUPPORTED_DOC_FORMATS:
            table.add_row(fmt)
        console.print(table)

    elif format_type == "audio":
        from ..utils.formats import SUPPORTED_AUDIO_FORMATS_SHOW

        console.print(
            Panel(SUPPORTED_AUDIO_FORMATS_SHOW, title="Supported Audio Formats")
        )

    elif format_type == "video":
        from ..utils.formats import SUPPORTED_VIDEO_FORMATS_SHOW

        console.print(
            Panel(SUPPORTED_VIDEO_FORMATS_SHOW, title="Supported Video Formats")
        )

    elif format_type == "image":
        from ..utils.formats import SUPPORTED_IMAGE_FORMATS_SHOW

        console.print(
            Panel(SUPPORTED_IMAGE_FORMATS_SHOW, title="Supported Image Formats")
        )


# Audio Effects (via audiobot)
@cli.command(name="audio-effects")
@click.argument("args", nargs=-1)
def audio_effects(args):
    """Apply audio effects and voice changes"""

    try:
        audiobot_cli(list(args))
    except NameError:
        console.print("[bold red]Error:[/] audiobot module not available")


# Main entry point
def main():
    """Main entry point with error handling"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/]")
        sys.exit(0)
    except FilemacError as e:
        console.print(f"[bold red]Filemac Error:[/] {str(e)}")
        sys.exit(1)
    except FileSystemError as e:
        console.print(f"[bold red]File System Error:[/] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {str(e)}")
        logger.critical(f"Critical failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
