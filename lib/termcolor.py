#! /usr/bin/env python3
from enum import Enum, unique


def write(message, *args, **kwargs):
    '''Prints a formated message'''

    formated_args = __format_args(*args)

    print('[{}m{}[0m'.format(formated_args, message), **kwargs)

def __format_args(*args):
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
    BOLD = '01'
    ITALIC = '03'
    UNDER = '04'
    BLINK = '05'
    REVERSE = '07'


@unique
class Font(Enum):
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
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    GRAY = 47
