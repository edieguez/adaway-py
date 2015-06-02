#! /usr/bin/env python3
"""A python3 script to block publicity."""
from sys import argv, exit
from lib.config import Config
from lib.database import Database
from lib.validator import parse_args

args = parse_args()

config = Config()
config.create()

database = Database()

# Deactivate
if args.d:
    database.export(True)
    exit(0)

args.u = not database.create() or args.u

# Update or populate the database
if not args.a or args.u:
    database.populate()


if not args.u or args.a or not argv[1:]:
    database.export(args.filename)
