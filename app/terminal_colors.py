import os
import sys

from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()


def _colorize(message: str, color: str) -> str:
    if os.getenv("NO_COLOR") is not None or not sys.stdout.isatty():
        return message
    return f"{color}{message}{Style.RESET_ALL}"


def success(message: str) -> str:
    return _colorize(message, Fore.GREEN)


def error(message: str) -> str:
    return _colorize(message, Fore.RED)


def info(message: str) -> str:
    return _colorize(message, Fore.CYAN)