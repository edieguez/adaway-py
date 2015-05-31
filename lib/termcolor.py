"""A simple class to print in colors."""

from lib.colorama.initialise import init


init()


class Termcolor:

    """An object to print using color in the terminal."""

    @classmethod
    def write(cls, message, *args):
        """Print a formated message."""
        formated_args = cls.__format_args(*args)

        print(cls)
        print(message)
        print(formated_args)
        print('[{}m{}[0m'.format(formated_args, message))

    @staticmethod
    def __format_args(*args):
        formated_args = '00'

        if args:
            formated_args = ';'.join(args)

        return formated_args


class Format():

    """Enum containing the format numeric codes."""

    BOLD = '01'
    ITALIC = '03'
    UNDER = '04'
    BLINK = '05'
    REVERSE = '07'


class Font():

    """Enum containing the font numeric codes."""

    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    PURPLE = "35"
    CYAN = "36"
    GRAY = "37"
    WHITE = "38"


class Background():

    """Enum containing the background numeric codes."""

    BLACK = "40"
    RED = "41"
    GREEN = "42"
    YELLOW = "43"
    BLUE = "44"
    PURPLE = "45"
    CYAN = "46"
    GRAY = "47"
