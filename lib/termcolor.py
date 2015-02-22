"""A simple class to print in colors."""

from enum import Enum, unique

from lib.colorama.initialise import init


init()


class Termcolor:

    """An object to print using color in the terminal."""

    def write(self, message, *args, **kwargs):
        """Print a formated message."""
        formated_args = self.__format_args(*args)

        print('[{}m  {}[0m'.format(formated_args, message), **kwargs)

    def __format_args(self, *args):
        formated_args = '00'

        if args:
            aux_list = list()

            for arg in args:
                if isinstance(arg, Enum):
                    arg = arg.value

                if str(arg).isdigit():
                    aux_list.append(str(arg))
                else:
                    raise ValueError('The format arguments must be numeric values')

            formated_args = ';'.join(aux_list)

        return formated_args


@unique
class Format(Enum):

    """Enum containing the format numeric codes."""

    BOLD = '01'
    ITALIC = '03'
    UNDER = '04'
    BLINK = '05'
    REVERSE = '07'


@unique
class Font(Enum):

    """Enum containing the font numeric codes."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    GRAY = 37
    WHITE = 38


@unique
class Background(Enum):

    """Enum containing the background numeric codes."""

    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    GRAY = 47
