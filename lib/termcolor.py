"""A simple class to print in colors."""

from colorama import init, Fore


class Termcolor:
    """An object to print using color in the terminal."""

    def __init__(self):
        init(True)

    def info(self, message):
        self._write(f'[i] {message}', Fore.BLUE)

    def warn(self, message):
        self._write(f'[w] {message}', Fore.YELLOW)

    def error(self, message):
        self._write(f'[e] {message}', Fore.RED)

    def _write(self, message, format_):
        """Print a formatted message."""

        print(f'  {format_}{message}')
