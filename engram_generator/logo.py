"""ASCII art logo for Engram Generator with optional ANSI colour."""

LOGO_PLAIN = r"""
  _____ _   _  ____ ____      _    __  __
 | ____| \ | |/ ___|  _ \    / \  |  \/  |
 |  _| |  \| | |  _| |_) |  / _ \ | |\/| |
 | |___| |\  | |_| |  _ <  / ___ \| |  | |
 |_____|_| \_|\____|_| \_\/_/   \_\_|  |_|
          G E N E R A T O R
""".strip("\n")

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_CYAN = "\033[36m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"

LOGO_COLOUR = (
    f"{_BOLD}{_CYAN}  _____ _   _  ____ ____      _    __  __{_RESET}\n"
    f"{_BOLD}{_CYAN} | ____| \\ | |/ ___|  _ \\    / \\  |  \\/  |{_RESET}\n"
    f"{_BOLD}{_BLUE} |  _| |  \\| | |  _| |_) |  / _ \\ | |\\/| |{_RESET}\n"
    f"{_BOLD}{_BLUE} | |___| |\\  | |_| |  _ <  / ___ \\| |  | |{_RESET}\n"
    f"{_BOLD}{_MAGENTA} |_____|_| \\_|\\____|_| \\_\\/_/   \\_\\_|  |_|{_RESET}\n"
    f"{_DIM}          G E N E R A T O R{_RESET}"
)


def print_logo(colour: bool = True) -> None:
    """Print the Engram Generator logo to stdout.

    Args:
        colour: If True, use ANSI colour codes. If False, plain text.
    """
    print(LOGO_COLOUR if colour else LOGO_PLAIN)
