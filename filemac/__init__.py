# FileMAC Package
# Main package initialization
from pathlib import Path
__version__ = open(Path(__file__).parent.parent / "version.txt").read().strip()

# Import the main CLI functions
from .cli.cli import argsdev as filemac_cli
from .cli.app import enhanced_argsdev as filemac_app

# Audiobot CLI (if available)
try:
    from audiobot.cli import cli as audiobot_cli
except ImportError:
    audiobot_cli = None

# Main entry points
__all__ = ["filemac_cli", "filemac_app", "audiobot_cli"]

# Aliases for backward compatibility
argsdev = filemac_cli
enhanced_argsdev = filemac_app
