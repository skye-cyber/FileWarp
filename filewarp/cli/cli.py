#!/usr/bin/env python3

import os
import sys

# from functools import lru_cache
from pathlib import Path

# Rich imports for amazing UI
from rich.panel import Panel
from rich.progress import Progress

# Click for better CLI handling
import click

# Local imports
from ..core.document import DocumentConverter
from ..core.pdf.core import PageExtractor
from ..core.exceptions import FileSystemError, FilemacError

# from ..utils.colors import fg, bg, rs
from ..utils.simple import logger
from ._entry_ import console
from .utils import (
    animate_processing,
    show_quick_commands,
    display_version,
    show_supported_formats,
    FileWarpGroup,
    with_format_table,
)

try:
    from audiobot.cli import cli as audiobot_cli
except ImportError:
    pass


# RESET = rs


@click.group(
    cls=FileWarpGroup,
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
        console.print(
            "\n[bold]Welcome to Filemac![/] Use [cyan]filewarp --help[/] for commands.\n"
        )
        show_quick_commands()


# Document Conversion Commands
@cli.command(name="convert-doc")
@with_format_table("document")
@click.argument("files", nargs=-1, required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
@click.option("--isolate", "-iso", help="Isolate specific file types")
@click.option(
    "--use-extras", "-X", is_flag=True, help="Use alternative conversion method"
)
@click.pass_context
# @animate_processing("Document conversion")
def convert_document(ctx, files, to, isolate, use_extras):
    """Convert documents between formats (PDF, DOCX, etc.)"""

    if files[0] == "help":
        from ..utils.formats import create_doc_formats_table

        create_doc_formats_table()
        # show_supported_formats("document")
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
@with_format_table("audio")
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
@with_format_table("video")
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
@with_format_table("image")
@click.argument("file", required=True)
@click.option("--to", "-tf", required=True, help="Target format for conversion")
# @animate_processing("Image conversion")
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
@click.argument("pages", nargs=-1, type=str, required=True)
@animate_processing("Page extraction")
def extract_pages(pdf_file, pages):
    """Extract specific pages from PDF"""

    console.print(f"[bold]Extracting pages[/] {pages} from [cyan]{pdf_file}[/]")

    args = [pdf_file] + [str(p) for p in pages]
    PageExtractor.run(args)


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


@cli.command(name="pdf2long-image")
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

    output = generate_filename(Path(svg_file), to)

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

    conv = DocumentConverter(document)
    conv.doc2image(to)


# HTML to Word
@cli.command(name="html2word")
@click.argument("html_files", nargs=-1, required=True)
@animate_processing("HTML to Word conversion")
def html_to_word(html_files):
    """Convert HTML files to Word documents"""

    from ..core.html import HTML2Word
    from ..utils.file_utils import generate_filename

    converter = HTML2Word()
    console.print(
        Panel(
            f"[bold]Converting[/] {len(html_files)} file(s) to [cyan]word[/]",
            border_style="green",
        )
    )
    for html_file in html_files:
        output = generate_filename(Path(html_file).absolute().parent, "docx")
        converter.convert_file(html_file, output)

        console.print(f"[bold green]✓[/] Converted: [cyan]{output}[/]")


# Markdown to Word
@cli.command(name="markdown2word")
@click.argument("markdown_file", required=True)
@animate_processing("Markdown to Word conversion")
def markdown_to_word(markdown_file):
    """Convert Markdown to Word with Mermaid rendering"""

    console.print(f"[bold]Converting[/] [cyan]{markdown_file}[/] to Word")


# Text to Word
@cli.command(name="text2word")
@click.argument("text_file", required=True)
@click.option("--font-size", default=12, help="Font size")
@click.option("--font-name", default="Times New Roman", help="Font name")
@animate_processing("Text to Word conversion")
def text_to_word(text_file, font_size, font_name):
    """Convert styled text to Word document"""

    from ..core.text.core import StyledText

    init = StyledText(text_file, None, font_size, font_name)
    init.text_to_word()


# Document Conversion Commands
@cli.command(name="edit-video")
@with_format_table("video")
@click.argument("files", nargs=-1, required=True)
@click.option("--range", "-r", type=str, help="Comma seperated ranges eg 0,30")
@click.option("--trim_start", type=int, help="Trim the first n seconds")
@click.option("--trim_end", type=int, help="Trim the last n seconds")
@click.option(
    "--quality",
    type=str,
    default="medium",
    help="Output video quality: ultrafast,fast,medium,slow,veryslow\n \
        Fast imply fast encoding hence large size",
)
@click.pass_context
def edit_video(ctx, files, range, trim_start, trim_end, quality):
    """Convert documents between formats (PDF, DOCX, etc.)"""

    if files[0] == "help":
        from ..utils.formats import create_video_formats_table

        return create_video_formats_table()

    console.print(
        Panel(
            f"[bold]Editing[/] {len(files)} file(s) by [cyan]triming[/]",
            border_style="green",
            expand=False,
        )
    )

    from ..core.video.Editor import VideoEditor
    from ..utils.file_utils import generate_filename
    from ..utils.decorators import for_loop
    # from ..core.video.models import VideoQuality

    editor = VideoEditor()

    # with Progress(console=console) as progress:
    # task = progress.add_task("[cyan]Editing...", total=len(files))

    # if len(files) == 1 and not Path(files[0]).is_dir():
    #     output_file = generate_filename(
    #         Path(files[0]).parent, Path(files[0]).suffix, ""
    #     )
    #     if trim_start:
    #         editor.trim_start(files[0], output_file, quality=quality)
    #     elif trim_end:
    #         editor.trim_end(files[0], output_file, quality=quality)
    #     elif range:
    #         trange = range.split(",")
    #         if len(tuple(trange)) > 1:
    #             editor.trim_video(
    #                 files[0], output_file, tuple(trange), quality=quality
    #             )
    #     console.print(f"File: {output_file}")
    # else:
    @for_loop(files)
    def process(self, file):
        try:
            file = Path(file)
            if file.exists():
                output_file = generate_filename(file.parent, file.suffix.strip("."), "")
                if trim_start:
                    editor.trim_start(file, output_file, trim_start, quality=quality)
                elif trim_end:
                    editor.trim_end(file, output_file, trim_end, quality=quality)
                elif range:
                    trange = [int(r) for r in range.split(",")]
                    if len(tuple(trange)) == 1:
                        trange = [0, trange[0]]

                    editor.trim_video(file, output_file, tuple(trange), quality=quality)
        except Exception as e:
            print(e)

    process(None)


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
        raise
        console.print(f"[bold red]Unexpected Error:[/] {str(e)}")
        logger.critical(f"Critical failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
