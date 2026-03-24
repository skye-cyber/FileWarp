from rich.console import Console
from rich.panel import Panel
from rich.align import Align

import importlib.metadata

try:
    __version__ = importlib.metadata.version("filewarp")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

# ASCII Art Banner
BANNER_old = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███████╗██╗██╗     ███████╗███╗   ███╗ █████╗  ██████╗    ║
║    ██╔════╝██║██║     ██╔════╝████╗ ████║██╔══██╗██╔════╝    ║
║    █████╗  ██║██║     █████╗  ██╔████╔██║███████║██║         ║
║    ██╔══╝  ██║██║     ██╔══╝  ██║╚██╔╝██║██╔══██║██║         ║
║    ██║     ██║███████╗███████╗██║ ╚═╝ ██║██║  ██║╚██████╗    ║
║    ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝    ║
║                                                              ║
║                 File Management & Conversion                 ║
║                   Version {__version__} • 2026                       ║
╚══════════════════════════════════════════════════════════════╝
"""


BANNER = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ███████╗██╗██╗     ███████╗██╗    ██╗ █████╗ ██████╗ ██████╗              ║
║    ██╔════╝██║██║     ██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗             ║
║    █████╗  ██║██║     █████╗  ██║ █╗ ██║███████║██████╔╝██████╔╝             ║
║    ██╔══╝  ██║██║     ██╔══╝  ██║███╗██║██╔══██║██╔══██╗██╔═══╝              ║
║    ██║     ██║███████╗███████╗╚███╔███╔╝██║  ██║██║  ██║██║                  ║
║    ╚═╝     ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                  ║
║                                                                              ║
║                                                                              ║
║                        File Warpping & Conversion Tool                       ║
║                           Version {__version__} • 2026                               ║
║                                                                              ║
║          ╔══════════════════════════════════════════════════════╗            ║
║          ║  Warp • Convert • Compress • Encrypt • Transform     ║            ║
║          ╚══════════════════════════════════════════════════════╝            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Modern Minimalist Banner for FileWarp

BANNER_v1 = f"""
╭──────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│    ┌─┐┬ ┬┌┐┌┬─┐┌┬┐┌─┐┬ ┬  ┬ ┬┌─┐┬ ┬┌─┐                                    │
│    │  │ ││││├┬┘ ││├┤ └┬┘  │││├─┤└┬┘├┤                                     │
│    └─┘└─┘┘└┘┴└──┴┘└─┘ ┴   └┴┘┴ ┴ ┴ └─┘                                    │
│                                                                              │
│    ╭──────────────────────────────────────────────────────────────────────╮ │
│    │                       FILE WRAP v{__version__}                                │ │
│    │              The Ultimate File Warpping Solution                      │ │
│    ╰──────────────────────────────────────────────────────────────────────╯ │
│                                                                              │
│    📦  Wrap files in containers   🔒  Encrypt sensitive data                │
│    🗜️  Compress with smart algorithms  🔄  Convert between formats          │
│    📤  Batch process thousands of files  🎨  Preserve metadata              │
│                                                                             │
│    ⚡  "Wrap it once, use it everywhere"  ⚡                                 │
│                                                                             │
│    🌐  github.com/skye-cyber filewarp  |  📚  Documentation: filewarp.io     │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
"""

# Cyberpunk Style Banner for FileWarp

BANNER_v2 = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ░▒▓███████▓▒░ ░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░ │
│    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ │
│    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        │
│    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░ ░▒▓█▓▒░      │
│    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     │
│    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░   ░▒▓█▓▒░    │
│    ░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░   ░▒▓█▓▒░   ░▒▓███████▓▒░ ░▒▓██████▓▒░  │
│                                                                             │
│    ╔══════════════════════════════════════════════════════════════════════╗ │
│    ║                    FILE WARP - CYBER EDITION                         ║ │
│    ║            Advanced File Warpping & Transformation System            ║ │
│    ╚══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│    ⚡ INITIALIZING CORE SYSTEMS...                                        ⚡ │
│    🔐 ENCRYPTION: ACTIVE    📦 WRAPPING: READY    🗜️ COMPRESSION: ONLINE     │
│    📊 MEMORY: 42GB ALLOCATED    🔋 POWER: 100%                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""


BANNER_v3 = f"""
╭──────────────────────────────────────────────────────────────────────────╮
│                                                                          │
│    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲          │
│                                                                          │
│                           F I L E   W R A P                              │
│                                                                          │
│    ╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱          │
│                                                                          │
│    📦  Wrap files into containers      🔄  Convert between formats        │
│    🗜️  Smart compression algorithms    🔒  AES-256 encryption             │
│    📤  Batch processing                🏷️  Metadata preservation          │
│                                                                          │
│    ╭────────────────────────────────────────────────────────────────╮    │
│    │  "Your files, perfectly warpped, every time."                  │    │
│    ╰────────────────────────────────────────────────────────────────╯    │
│                                                                          │
│    Version {__version__}  |  MIT License  |  github.com/skye-cyber/filewarp                 │
│                                                                          │
╰──────────────────────────────────────────────────────────────────────────╯
"""

console = Console()


def display_banner():
    """Display the FileWarp banner with Rich styling"""
    console.print(
        Align.left(
            Panel(
                BANNER,
                border_style="cyan",
                padding=(1, 2),
                title="[bold cyan]FileWarp[/]",
                subtitle=f"[dim]v{__version__}[/]",
            )
        )
    )
    console.print()  # Empty line for spacing


def display_banner_simple():
    """Display the animated banner"""
    console.print(BANNER, style="bold cyan", justify="center")
    console.print("─" * console.width, style="dim")
