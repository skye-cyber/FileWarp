from rich.console import Console
from rich.theme import Theme

# Initialize rich console with custom theme
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "red bold",
        "success": "green bold",
        "file": "blue",
        "dir": "magenta",
        "command": "yellow bold",
        "arg": "cyan",
    }
)

console = Console(theme=custom_theme)
