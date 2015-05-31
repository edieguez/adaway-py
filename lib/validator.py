"""A module to validate the write permission."""
import os
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='A python3 script to block publicity')
    parser.add_argument('-o', dest='filename', help='output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='apply blocking')
    group.add_argument('-d', action='store_true', help='deactivate blocking')
    group.add_argument('-u', action='store_true', help='update database')

    return parser.parse_args()

def validate_write_permission(filename):
    """Validate the write permission.

    Returns True if the file or directory is writable
    """
    parent_dir = os.path.dirname(filename) or '.'

    if os.path.exists(filename):
        return os.access(filename, os.W_OK)
    elif os.path.exists(parent_dir):
        return os.access(parent_dir, os.W_OK)

    return os.access(filename, os.W_OK)
