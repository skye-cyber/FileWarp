# multimedia_cli/formats.py
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns

try:
    from cli._entry_ import console
except ImportError:
    from rich.console import Console

    console = Console()

# Color mappings for consistent styling
STYLES = {
    "input": "bold cyan",
    "output": "bold green",
    "arrow": "yellow",
    "pending": "dim italic red",
    "header": "bold white on blue",
    "format": "magenta",
}


def create_doc_formats_table():
    """Create an elegant table for document formats"""
    table = Table(
        title="[bold]Document Format Conversions[/]",
        title_style="bold cyan",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold white on blue",
        show_lines=True,
        padding=(0, 2),
    )

    table.add_column("Input Format", style="bold cyan", justify="center")
    table.add_column("→", style="yellow", justify="center", width=3)
    table.add_column("Output Formats", style="green", justify="left")

    conversions = [
        ("xlsx", "→", "csv, txt, doc/docx, db(sql)"),
        ("doc/docx", "→", "txt, pdf, ppt/pptx, audio(ogg)"),
        ("txt", "→", "pdf, docx/doc, audio(ogg)"),
        ("pdf", "→", "doc/docx, txt, audio(ogg)"),
        ("pptx/ppt", "→", "doc/docx"),
    ]

    for in_fmt, arrow, out_fmt in conversions:
        table.add_row(in_fmt, arrow, out_fmt)

    return table


def create_audio_formats_table():
    """Create an elegant table for audio formats"""
    table = Table(
        title="[bold]Supported Audio Formats[/]",
        title_style="bold cyan",
        box=box.ROUNDED,
        border_style="magenta",
        header_style="bold white on magenta",
        show_header=False,
        padding=(0, 3),
    )

    table.add_column("Format", style="bold magenta", justify="center")
    table.add_column("Status", style="white", justify="center")

    audio_formats = [
        ("WAV", "✅ Supported"),
        ("MP3", "✅ Supported"),
        ("OGG", "✅ Supported"),
        ("FLV", "✅ Supported"),
        ("OGV", "✅ Supported"),
        ("MOV", "✅ Supported"),
        ("WEBM", "✅ Supported"),
        ("AAC", "⏳ Pending Implementation"),
        ("BPF", "⏳ Pending Implementation"),
        ("M4A", "✅ Supported"),
        ("RAW", "✅ Supported"),
        ("AIFF", "✅ Supported"),
        ("FLAC", "✅ Supported"),
    ]

    for fmt, status in audio_formats:
        table.add_row(fmt, status)

    return table


def create_video_formats_table():
    """Create an elegant table for video formats"""
    table = Table(
        title="[bold]Supported Video Formats[/]",
        title_style="bold cyan",
        box=box.ROUNDED,
        border_style="green",
        header_style="bold white on green",
        show_lines=True,
    )

    table.add_column("Format", style="bold green", justify="center")
    table.add_column("Codec", style="cyan", justify="center")
    table.add_column("Status", style="white", justify="center")

    video_formats = [
        ("MP4", "mpeg4", "✅ Supported"),
        ("AVI", "rawvideo", "✅ Supported"),
        ("OGV", "avc", "⏳ Pending Implementation"),
        ("WEBM", "libvpx", "✅ Supported"),
        ("MOV", "mpeg4", "✅ Supported"),
        ("MKV", "mpeg4", "✅ Supported"),
        ("FLV", "flv", "✅ Supported"),
        ("WMV", "WMV", "⏳ Pending Implementation"),
    ]

    for fmt, codec, status in video_formats:
        table.add_row(fmt, codec, status)

    return table


def create_image_formats_table():
    """Create an elegant table for image formats"""
    table = Table(
        title="[bold]Supported Image Formats[/]",
        title_style="bold cyan",
        box=box.ROUNDED,
        border_style="yellow",
        header_style="bold white on yellow",
        show_lines=True,
    )

    table.add_column("Format", style="bold yellow", justify="center")
    table.add_column("Extension", style="cyan", justify="center")
    table.add_column("Status", style="white", justify="center")

    image_formats = [
        ("JPEG", ".jpeg", "✅ Supported"),
        ("JPG", ".jpg", "✅ Supported"),
        ("PNG", ".png", "✅ Supported"),
        ("GIF", ".gif", "✅ Supported"),
        ("BMP", ".bmp", "✅ Supported"),
        ("DIB", ".dib", "✅ Supported"),
        ("TIFF", ".tiff", "✅ Supported"),
        ("PIC", ".pic", "✅ Supported"),
        ("PDF", ".pdf", "✅ Supported"),
        ("WEBP", ".webp", "✅ Supported"),
        ("ICNS", ".icns", "✅ Supported"),
        ("EPS", ".eps", "✅ Supported"),
        ("PSD", ".psd", "⏳ Pending Implementation"),
        ("SVG", ".svg", "⏳ Pending Implementation"),
        ("EXR", ".exr", "⏳ Pending Implementation"),
        ("DXF", ".dxf", "⏳ Pending Implementation"),
        ("PICT", ".pct", "⏳ Pending Implementation"),
        ("PS", ".ps", "⏳ Pending Implementation"),
        ("POSTSCRIPT", ".ps", "⏳ Pending Implementation"),
    ]

    for fmt, ext, status in image_formats:
        table.add_row(fmt, ext, status)

    return table


def create_quick_reference():
    """Create a quick reference panel with all formats"""
    doc_table = create_doc_formats_table()
    audio_table = create_audio_formats_table()
    video_table = create_video_formats_table()
    image_table = create_image_formats_table()

    # Create panels for each category
    doc_panel = Panel(
        doc_table, title="📄 Documents", border_style="blue", padding=(1, 2)
    )

    audio_panel = Panel(
        audio_table, title="🎵 Audio", border_style="magenta", padding=(1, 2)
    )

    video_panel = Panel(
        video_table, title="🎬 Video", border_style="green", padding=(1, 2)
    )

    image_panel = Panel(
        image_table, title="🖼️ Images", border_style="yellow", padding=(1, 2)
    )

    # Arrange in columns for compact display
    top_row = Columns([doc_panel, audio_panel], equal=True, expand=True)
    bottom_row = Columns([video_panel, image_panel], equal=True, expand=True)

    return Panel(
        Columns([top_row, bottom_row], equal=False),
        title="[bold cyan]File Format Support Matrix[/]",
        border_style="bright_white",
        padding=(1, 2),
    )


def create_formats_help():
    """Create a comprehensive help display for formats"""
    help_text = Text()
    help_text.append("\n📋 ", style="bold blue")
    help_text.append("Format Conversion Guide\n\n", style="bold white")

    help_text.append("  ✅ ", style="green")
    help_text.append("Fully implemented and tested\n", style="white")

    help_text.append("  ⏳ ", style="yellow")
    help_text.append("Pending implementation (coming soon)\n\n", style="dim")

    help_text.append("  🔄 ", style="cyan")
    help_text.append("Batch conversions supported\n", style="white")

    help_text.append("  🎯 ", style="magenta")
    help_text.append("Preserves metadata where applicable\n\n", style="white")

    help_text.append("  💡 ", style="bright_yellow")
    help_text.append("Tip: Use ", style="white")
    help_text.append("--help ", style="bold cyan")
    help_text.append("with any command for specific format options", style="white")

    return Panel(
        help_text, title="[bold]Format Help[/]", border_style="cyan", padding=(1, 2)
    )


# Export the table creation functions
__all__ = [
    "create_doc_formats_table",
    "create_audio_formats_table",
    "create_video_formats_table",
    "create_image_formats_table",
    "create_quick_reference",
    "create_formats_help",
]

# For backward compatibility, also provide the original constants
# But now as formatted strings for legacy code
SUPPORTED_DOC_FORMATS_SHOW = """
Document Format Conversions:
  xlsx     → csv, txt, doc/docx, db(sql)
  doc/docx → txt, pdf, ppt/pptx, audio(ogg)
  txt      → pdf, docx/doc, audio(ogg)
  pdf      → doc/docx, txt, audio(ogg)
  pptx/ppt → doc/docx
"""

SUPPORTED_AUDIO_FORMATS = [
    "wav",
    "mp3",
    "ogg",
    "flv",
    "ogv",
    "webm",
    "aiff",
    "flac",
    "m4a",
    "raw",
    "bpf",
    "aac",
]

SUPPORTED_AUDIO_FORMATS_DIRECT = [
    "mp3",
    "wav",
    "raw",
    "ogg",
    "aiff",
    "flac",
    "flv",
    "webm",
    "ogv",
]

SUPPORTED_AUDIO_FORMATS_SHOW = """
Supported Audio Formats:
  • WAV   • MP3   • OGG   • FLV   • OGV
  • MOV   • WEBM  • AAC*  • BPF*  • M4A
  • RAW   • AIFF  • FLAC

  * Pending Implementation
"""

SUPPORTED_VIDEO_FORMATS = ["MP4", "AVI", "OGV", "WEBM", "MOV", "MKV", "FLV", "WMV"]

Video_codecs = {
    "MP4": "mpeg4",
    "AVI": "rawvideo",
    "WEBM": "libvpx",
    "MOV": "mpeg4",
    "MKV": "mpeg4",
    "FLV": "flv",
}

SUPPORTED_VIDEO_FORMATS_SHOW = """
Supported Video Formats:
  • MP4  (mpeg4)     • AVI  (rawvideo)
  • OGV* (avc)       • WEBM (libvpx)
  • MOV  (mpeg4)     • MKV  (mpeg4)
  • FLV  (flv)       • WMV* (WMV)

  * Pending Implementation
"""

SUPPORTED_IMAGE_FORMATS = {
    "JPEG": ".jpeg",
    "JPG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "BMP": ".bmp",
    "DIB": ".dib",
    "TIFF": ".tiff",
    "PIC": ".pic",
    "PDF": ".pdf",
    "WEBP": ".webp",
    "EPS": ".eps",
    "ICNS": ".icns",
    "PSD": ".psd",
    "SVG": ".svg",
    "EXR": ".exr",
    "DXF": ".dxf",
    "PICT": ".pct",
    "PS": ".ps",
    "POSTSCRIPT": ".ps",
}

SUPPORTED_IMAGE_FORMATS_SHOW = """
Supported Image Formats:
  • JPEG (.jpeg)  • JPG  (.jpg)   • PNG  (.png)
  • GIF  (.gif)   • BMP  (.bmp)   • DIB  (.dib)
  • TIFF (.tiff)  • PIC  (.pic)   • PDF  (.pdf)
  • WEBP (.webp)  • ICNS (.icns)  • EPS  (.eps)
  • PSD* (.psd)   • SVG* (.svg)   • EXR* (.exr)
  • DXF* (.dxf)   • PICT*(.pct)   • PS*  (.ps)

  * Pending Implementation
"""

SUPPORTED_DOCUMENT_FORMATS = [
    "pdf",
    "doc",
    "docx",
    "csv",
    "xlsx",
    "xls",
    "ppt",
    "pptx",
    "txt",
    "ogg",
    "mp3",
    "audio",
]


# Function to display all formats in a beautiful layout
def display_all_formats():
    """Display all format tables in a beautiful layout"""

    console.print("\n")
    console.print(create_quick_reference())
    console.print("\n")
    console.print(create_formats_help())
    console.print("\n")
