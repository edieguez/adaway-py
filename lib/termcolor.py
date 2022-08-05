"""A simple class to print in colors."""

from colorama import init, Fore, Style


class Termcolor:

    """An object to print using color in the terminal."""

    def __init__(self):
        init()

    def info(self, message):
        self.__write(f'[i] {message}', Fore.BLUE)

    def warn(self, message):
        self.__write(f'[w] {message}', Fore.YELLOW)

    def error(self, message):
        self.__write(f'[e] {message}', Fore.RED)

    def __write(self, message, format):

        """Print a formatted message."""

        print(f'  {format}{message}{Style.RESET_ALL}')
