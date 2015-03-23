"""A module to validate the write permission."""
import os
from sys import argv


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
