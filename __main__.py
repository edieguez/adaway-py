#! /usr/bin/env python
"""A python3 script to block publicity."""

import os
import sys
from argparse import ArgumentParser

from lib import config
from lib.database import Database
from lib.termcolor import Termcolor

# Argument parsing
parser = ArgumentParser(description='A python3 script to block publicity')
parser.add_argument('-o', dest='filename', help='output file')

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true', help='apply blocking')
group.add_argument('-d', action='store_true', help='deactivate blocking')
group.add_argument('-u', action='store_true', help='update database')

args = parser.parse_args()

config.write()

database = Database()

if args.d:
    database.export(None, True)
    sys.exit(0)

args.u = not database.create()

if not args.a or args.u:
    database.populate()

if not args.u or args.a or not sys.argv[1:]:
    database.export(args.filename)
