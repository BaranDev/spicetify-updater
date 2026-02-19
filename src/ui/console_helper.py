import sys

APP_NAME = "Spicetify Updater"
APP_VERSION = "2.0.0"

# ANSI color codes (fallback gracefully on terminals that don't support them)
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def print_header():
    """Print a compact application header."""
    print(f"\n{_BOLD}{_CYAN}{APP_NAME} v{APP_VERSION}{_RESET}")
    print(f"{'-' * 35}\n")


def print_status(message):
    """Print a status/info message."""
    print(f"  {_CYAN}>{_RESET} {message}")


def print_success(message):
    """Print a success message."""
    print(f"  {_GREEN}OK{_RESET} {message}")


def print_error(message):
    """Print an error message."""
    print(f"  {_RED}ERROR{_RESET} {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"  {_YELLOW}!{_RESET} {message}")


def ask_yes_no(question, default_yes=True):
    """Prompt the user with a yes/no question. Returns True for yes, False for no."""
    hint = "Y/n" if default_yes else "y/N"
    try:
        answer = input(f"\n  {question} [{hint}]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return default_yes

    if answer == "":
        return default_yes
    return answer in ("y", "yes")


def press_enter_to_exit(code=0):
    """Wait for the user to press Enter, then exit."""
    try:
        input(f"\n  Press Enter to exit...")
    except (EOFError, KeyboardInterrupt):
        pass
    sys.exit(code)
